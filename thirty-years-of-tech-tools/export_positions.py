#!/usr/bin/env python3
"""Position-grain export: one row per (position, skill).

Needed because two things cannot be done from year-level aggregates:

  * A SPLIT-HALF NULL. Resampling from a year's own aggregate treats that
    aggregate as the truth, so it cannot see the error in the aggregate itself
    -- which is exactly the error that makes thin early years look like they
    churn faster. Splitting a year's POSITIONS into two random halves and
    comparing them does capture it.

  * VERBOSITY STRATIFICATION. Skills per position drifts 4.5 -> 6.7 across the
    window. Whether skill concentration really rose can only be answered by
    holding that constant, i.e. comparing positions with the same skill count.

Emits (pos_hash, yr, mon, role, sen, prec, dst_id). pos_hash is md5 of the
position key, so nothing person-identifying leaves the host.
"""
from __future__ import annotations
import json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "_data"

SQL = """
  SELECT md5(src_id || '|' || coalesce(properties_json->>'companyEntityId','') || '|' || start_date) AS pos,
         substring(start_date from 1 for 4)::int AS yr,
         substring(start_date from 6 for 2) AS mon,
         properties_json->>'role' AS role,
         properties_json->>'seniorityLevel' AS sen,
         properties_json->>'startDatePrecision' AS prec,
         dst_id
  FROM skillenai_pii.talent_edges
  WHERE edge_type='HAS_SKILL' AND start_date ~ '^(199|200|201|202)[0-9]'
"""


def aws(profile: str, *a: str) -> str:
    r = subprocess.run(["aws", "--profile", profile, "--region", "us-east-1", *a],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"aws {' '.join(a[:3])}: {r.stderr[:500]}")
    return r.stdout


def main() -> int:
    env = "prod"
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
    sql = " ".join(SQL.split())
    cmds = [
        "set -euo pipefail",
        "rm -rf /tmp/skpos && install -d -o postgres -m 700 /tmp/skpos",
        f"sudo -u postgres psql -d skillenai -v ON_ERROR_STOP=1 -c "
        f"\"\\copy ({sql}) TO PROGRAM 'gzip -c > /tmp/skpos/positions.csv.gz' WITH (FORMAT csv, HEADER)\"",
        f"aws s3 cp /tmp/skpos/positions.csv.gz s3://{bucket}/{prefix}/positions.csv.gz --region us-east-1",
        "ls -l /tmp/skpos", "rm -rf /tmp/skpos",
    ]
    cid = json.loads(aws(profile, "ssm", "send-command", "--instance-ids", iid,
                         "--document-name", "AWS-RunShellScript",
                         "--comment", "skn-insights skill-race position grain",
                         "--timeout-seconds", "7200",
                         "--parameters", json.dumps({"commands": cmds, "executionTimeout": ["7200"]}),
                         "--query", "Command.CommandId", "--output", "json"))
    print(f"ssm {cid} -> s3://{bucket}/{prefix}/positions.csv.gz", flush=True)
    for _ in range(1440):
        time.sleep(15)
        inv = json.loads(aws(profile, "ssm", "get-command-invocation",
                             "--command-id", cid, "--instance-id", iid))
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    print(f"status={inv['Status']}\n{inv['StandardOutputContent'][-1500:]}")
    if inv["Status"] != "Success":
        print("STDERR:\n" + inv["StandardErrorContent"][-2000:])
        return 1
    aws(profile, "s3", "cp", f"s3://{bucket}/{prefix}/positions.csv.gz",
        str(DATA / "positions.csv.gz"))
    print(f"pulled positions.csv.gz ({(DATA/'positions.csv.gz').stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
