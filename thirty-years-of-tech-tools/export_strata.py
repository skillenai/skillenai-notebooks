#!/usr/bin/env python3
"""SKI-611 robustness: per-year skill shares stratified by CAREER LENGTH.

SKI-611 records that profiles with 11+ positions return ~11.5 fewer skills under
per-position extraction, cause unknown, and warns the loss "biases toward recent
positions if the loss is concentrated in older ones". Long careers are exactly
the profiles that carry 1990s positions, so if that bias is real and ordinal,
this analysis inherits it.

Test: recompute everything within strata of the person's total position count.
If the 1998 composition and the extinction pattern are the same for people with
4-6 positions as for people with 11+, the bias does not reach the shares.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "_data"

SQL = """
  WITH p AS (
    SELECT DISTINCT src_id, properties_json->>'companyEntityId' AS cid, start_date
    FROM skillenai_pii.talent_edges
    WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'),
  n AS (SELECT src_id, count(*) AS npos FROM p GROUP BY src_id),
  e AS (
    SELECT t.src_id, t.properties_json->>'companyEntityId' AS cid, t.start_date,
           t.dst_id, substring(t.start_date from 1 for 4)::int AS yr
    FROM skillenai_pii.talent_edges t
    WHERE t.edge_type='HAS_SKILL' AND t.start_date ~ '^(199|200|201|202)[0-9]')
  SELECT e.yr,
         CASE WHEN n.npos <= 3 THEN 'a_1_3' WHEN n.npos <= 6 THEN 'b_4_6'
              WHEN n.npos <= 10 THEN 'c_7_10' ELSE 'd_11plus' END AS band,
         e.dst_id,
         count(DISTINCT (e.src_id, e.cid, e.start_date)) AS n_pos
  FROM e JOIN n ON n.src_id = e.src_id
  GROUP BY 1,2,3
"""

DENOM = """
  WITH p AS (
    SELECT DISTINCT src_id, properties_json->>'companyEntityId' AS cid, start_date,
           substring(start_date from 1 for 4)::int AS yr
    FROM skillenai_pii.talent_edges
    WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'),
  n AS (SELECT src_id, count(*) AS npos FROM p GROUP BY src_id)
  SELECT p.yr,
         CASE WHEN n.npos <= 3 THEN 'a_1_3' WHEN n.npos <= 6 THEN 'b_4_6'
              WHEN n.npos <= 10 THEN 'c_7_10' ELSE 'd_11plus' END AS band,
         count(*) AS n_pos, count(DISTINCT p.src_id) AS n_people
  FROM p JOIN n ON n.src_id = p.src_id GROUP BY 1,2
"""

EXPORTS = {"strata_skill": SQL, "strata_denom": DENOM}


def aws(profile, *a):
    r = subprocess.run(["aws", "--profile", profile, "--region", "us-east-1", *a],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"aws {' '.join(a[:3])}: {r.stderr[:400]}")
    return r.stdout


def main():
    profile = "skillenai-prod"
    DATA.mkdir(parents=True, exist_ok=True)
    acct = aws(profile, "sts", "get-caller-identity", "--query", "Account", "--output", "text").strip()
    bucket = f"cdk-hnb659fds-assets-{acct}-us-east-1"
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    prefix = f"postgres-host-exports/prod/skill-race/{stamp}"
    iid = json.loads(aws(profile, "ec2", "describe-instances", "--filters",
                         "Name=tag:Name,Values=skn-prod-postgres",
                         "Name=instance-state-name,Values=running",
                         "--query", "Reservations[0].Instances[0].InstanceId", "--output", "json"))
    cmds = ["set -euo pipefail", "rm -rf /tmp/skst && install -d -o postgres -m 700 /tmp/skst"]
    for n, q in EXPORTS.items():
        s = " ".join(q.split())
        cmds.append(f"sudo -u postgres psql -d skillenai -v ON_ERROR_STOP=1 -c "
                    f"\"\\copy ({s}) TO PROGRAM 'gzip -c > /tmp/skst/{n}.csv.gz' WITH (FORMAT csv, HEADER)\"")
        cmds.append(f"aws s3 cp /tmp/skst/{n}.csv.gz s3://{bucket}/{prefix}/{n}.csv.gz --region us-east-1")
    cmds += ["ls -l /tmp/skst", "rm -rf /tmp/skst"]
    cid = json.loads(aws(profile, "ssm", "send-command", "--instance-ids", iid,
                         "--document-name", "AWS-RunShellScript", "--comment", "SKI-611 strata check",
                         "--timeout-seconds", "7200",
                         "--parameters", json.dumps({"commands": cmds, "executionTimeout": ["7200"]}),
                         "--query", "Command.CommandId", "--output", "json"))
    print(f"ssm {cid}", flush=True)
    for _ in range(1440):
        time.sleep(15)
        inv = json.loads(aws(profile, "ssm", "get-command-invocation", "--command-id", cid, "--instance-id", iid))
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    print("status=", inv["Status"])
    if inv["Status"] != "Success":
        print(inv["StandardErrorContent"][-2000:]); return 1
    for n in EXPORTS:
        aws(profile, "s3", "cp", f"s3://{bucket}/{prefix}/{n}.csv.gz", str(DATA / f"{n}.csv.gz"))
        print("pulled", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
