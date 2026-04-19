"""Phase C1: Naive median salary by skill.

"Reader-friendly" ranking: for each skill, what's the median salary of jobs requiring it?
No controls -- this conflates skill with seniority/role (that's the point to contrast with C2).

Runs pooled (all 3 roles) and per-role (DS, MLE only; AIE too thin).
"""
import csv
import numpy as np
from collections import defaultdict

CSV_IN = "jobs_merged.csv"
MIN_SALARY = 30000
MAX_SALARY = 800000
MIN_N = 20  # skill must appear in >= this many salaried jobs


def load():
    rows = []
    with open(CSV_IN) as f:
        for r in csv.DictReader(f):
            if r["salaryCurrency"] != "USD":
                continue
            if "US" not in r["country"]:
                continue
            try:
                lo = float(r["salaryMin"]); hi = float(r["salaryMax"])
            except (ValueError, TypeError):
                continue
            if lo <= 0 or hi <= 0 or hi < lo:
                continue
            mid = (lo + hi) / 2
            if mid < MIN_SALARY or mid > MAX_SALARY:
                continue
            skills = [s for s in (r["skills"] or "").split("|") if s]
            rows.append({
                "role": r["role_bucket"],
                "level": r["seniority"],
                "salary": mid,
                "skills": skills,
            })
    return rows


def rank(rows, label, out_csv):
    # Overall baseline
    all_sal = [r["salary"] for r in rows]
    baseline = np.median(all_sal)

    by_skill = defaultdict(list)
    for r in rows:
        for s in r["skills"]:
            by_skill[s].append(r["salary"])

    out = []
    for skill, sals in by_skill.items():
        if len(sals) < MIN_N:
            continue
        med = np.median(sals)
        out.append({
            "skill": skill,
            "n": len(sals),
            "median": round(med),
            "p25": round(np.percentile(sals, 25)),
            "p75": round(np.percentile(sals, 75)),
            "premium_vs_baseline": round(med - baseline),
            "premium_pct": round(100 * (med / baseline - 1), 1),
        })
    out.sort(key=lambda x: -x["premium_vs_baseline"])

    print(f"\n=== {label} (N={len(rows)}, baseline median ${baseline:,.0f}) ===")
    print(f"Top 20 by naive salary premium:")
    print(f"{'rank':>4} {'skill':30} {'N':>5} {'median':>10} {'prem$':>9} {'prem%':>6}")
    for i, r in enumerate(out[:20], 1):
        print(f"{i:>4} {r['skill'][:30]:30} {r['n']:>5} ${r['median']:>8,} ${r['premium_vs_baseline']:>+7,} {r['premium_pct']:>+5.1f}%")
    print(f"\nBottom 10 (discount):")
    for i, r in enumerate(out[-10:], 1):
        print(f"     {r['skill'][:30]:30} {r['n']:>5} ${r['median']:>8,} ${r['premium_vs_baseline']:>+7,} {r['premium_pct']:>+5.1f}%")

    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {out_csv}")
    return out


def main():
    rows = load()
    print(f"Total salaried US+USD jobs across DS/MLE/AIE: {len(rows)}")
    rank(rows, "POOLED (DS+MLE+AIE)", "phase_c1_pooled.csv")
    rank([r for r in rows if r["role"] == "DS"], "DS only", "phase_c1_ds.csv")
    rank([r for r in rows if r["role"] == "MLE"], "MLE only", "phase_c1_mle.csv")


if __name__ == "__main__":
    main()
