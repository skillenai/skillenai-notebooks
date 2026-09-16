#!/usr/bin/env python3
"""Export dated HAS_SKILL aggregates from prod Postgres via SSM (read-only).

Position key = (src_id, companyEntityId, start_date) -- the same key SKI-577
uses for the HAS_SKILL relationshipId, so one position maps to one row.

Denominator is positions THAT CARRY >=1 SKILL, not all positions: the 200-char
skills gate and the 61% attribution rate both vary, and dividing by all
positions would read those instrument properties as a skill trend.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "_data"

# Positions carrying >=1 skill, one row per (person, employer, start).
POS = """
  SELECT DISTINCT src_id, properties_json->>'companyEntityId' AS cid, start_date,
         substring(start_date from 1 for 4)::int AS yr,
         properties_json->>'role' AS role,
         properties_json->>'seniorityLevel' AS sen,
         properties_json->>'startDatePrecision' AS prec
  FROM skillenai_pii.talent_edges
  WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'
"""

EDGE = """
  SELECT src_id, properties_json->>'companyEntityId' AS cid, start_date, dst_id,
         substring(start_date from 1 for 4)::int AS yr
  FROM skillenai_pii.talent_edges
  WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'
"""

EXPORTS = {
    # 1. per (year, skill) position counts + names.  The main table.
    "skill_year": f"""
        WITH e AS ({EDGE})
        SELECT e.yr, e.dst_id, n.canonical_name,
               count(DISTINCT (e.src_id, e.cid, e.start_date)) AS n_pos,
               count(DISTINCT e.src_id) AS n_people
        FROM e LEFT JOIN skillenai.entities n ON n.entity_id = e.dst_id
        GROUP BY 1,2,3""",

    # 2. denominator: positions with >=1 skill, by year.  Also the evidence-density
    #    check (skills per position) -- if that drifts, top-skill share drifts with it.
    "pos_year": f"""
        WITH p AS ({POS})
        SELECT yr, count(*) AS n_pos, count(DISTINCT src_id) AS n_people,
               count(*) FILTER (WHERE prec='year') AS n_yearprec
        FROM p GROUP BY yr""",

    # 3. role attached to the position -- lets role churn and skill churn be
    #    computed on the SAME above-gate sub-population (the role post used all
    #    568K profiles; this cohort is the 178K that carry skills).
    "role_year": f"""
        WITH p AS ({POS})
        SELECT yr, role, count(*) AS n_pos
        FROM p WHERE role IS NOT NULL GROUP BY 1,2""",

    # 4. skill x role x year, restricted to skills with real volume, for cuts.
    "skill_year_role": f"""
        WITH e AS ({EDGE}),
        big AS (SELECT dst_id FROM e GROUP BY dst_id HAVING count(*) >= 400),
        pr AS (SELECT DISTINCT src_id, properties_json->>'companyEntityId' AS cid,
                      start_date, properties_json->>'role' AS role
               FROM skillenai_pii.talent_edges
               WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'
                 AND properties_json->>'role' IS NOT NULL)
        SELECT e.yr, pr.role, e.dst_id,
               count(DISTINCT (e.src_id, e.cid, e.start_date)) AS n_pos
        FROM e JOIN big ON big.dst_id = e.dst_id
        JOIN pr ON pr.src_id = e.src_id AND pr.start_date = e.start_date
             AND pr.cid IS NOT DISTINCT FROM e.cid
        GROUP BY 1,2,3""",
}


def aws(profile: str, *a: str) -> str:
    r = subprocess.run(["aws", "--profile", profile, "--region", "us-east-1", *a],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"aws {' '.join(a[:3])}: {r.stderr[:500]}")
    return r.stdout


def main() -> int:
    env = sys.argv[1] if len(sys.argv) > 1 else "prod"
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else list(EXPORTS)
    profile = f"skillenai-{env}"
    DATA.mkdir(parents=True, exist_ok=True)
    acct = aws(profile, "sts", "get-caller-identity", "--query", "Account", "--output", "text").strip()
    bucket = f"cdk-hnb659fds-assets-{acct}-us-east-1"
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    prefix = f"postgres-host-exports/{env}/skill-race/{stamp}"
    iid = json.loads(aws(profile, "ec2", "describe-instances",
                         "--filters", f"Name=tag:Name,Values=skn-{env}-postgres",
                         "Name=instance-state-name,Values=running",
                         "--query", "Reservations[0].Instances[0].InstanceId", "--output", "json"))

    cmds = ["set -euo pipefail",
            "rm -rf /tmp/skrace && install -d -o postgres -m 700 /tmp/skrace"]
    for n in names:
        sql = " ".join(EXPORTS[n].split())
        cmds.append(f"sudo -u postgres psql -d skillenai -v ON_ERROR_STOP=1 -c "
                    f"\"\\copy ({sql}) TO PROGRAM 'gzip -c > /tmp/skrace/{n}.csv.gz' WITH (FORMAT csv, HEADER)\"")
        cmds.append(f"aws s3 cp /tmp/skrace/{n}.csv.gz s3://{bucket}/{prefix}/{n}.csv.gz --region us-east-1")
    cmds += ["ls -l /tmp/skrace", "rm -rf /tmp/skrace"]

    cid = json.loads(aws(profile, "ssm", "send-command", "--instance-ids", iid,
                         "--document-name", "AWS-RunShellScript",
                         "--comment", "skn-insights skill-race read-only export",
                         "--timeout-seconds", "7200",
                         "--parameters", json.dumps({"commands": cmds, "executionTimeout": ["7200"]}),
                         "--query", "Command.CommandId", "--output", "json"))
    print(f"ssm {cid} on {iid} -> s3://{bucket}/{prefix}/", flush=True)
    for _ in range(1440):
        time.sleep(15)
        inv = json.loads(aws(profile, "ssm", "get-command-invocation",
                             "--command-id", cid, "--instance-id", iid))
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    print(f"status={inv['Status']}\n{inv['StandardOutputContent'][-2500:]}")
    if inv["StandardErrorContent"].strip():
        print("STDERR:\n" + inv["StandardErrorContent"][-2500:])
    if inv["Status"] != "Success":
        return 1
    for n in names:
        aws(profile, "s3", "cp", f"s3://{bucket}/{prefix}/{n}.csv.gz", str(DATA / f"{n}.csv.gz"))
        print(f"pulled {n}.csv.gz ({(DATA / f'{n}.csv.gz').stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
