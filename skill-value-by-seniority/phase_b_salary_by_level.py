"""Phase B: Salary distributions by (role x level) for DS / MLE / AIE.

US-only, USD-only, midpoint of (salaryMin, salaryMax).
Reports:
  - N, median, p25, p75, mean per (role, level)
  - Bootstrap 95% CI on median
  - Mann-Whitney U + rank-biserial r for each adjacent-level pair
"""
import csv
import numpy as np
from collections import defaultdict
from scipy import stats

CSV_IN = "jobs_merged.csv"
LEVEL_ORDER = ["entry", "mid", "senior", "staff"]
MIN_SALARY = 30000
MAX_SALARY = 800000
BOOT = 2000
RNG = np.random.default_rng(42)


def load():
    buckets = defaultdict(list)  # (role, level) -> [salary_midpoints]
    with open(CSV_IN) as f:
        for row in csv.DictReader(f):
            if row["salaryCurrency"] != "USD":
                continue
            if "US" not in row["country"]:
                continue
            try:
                lo = float(row["salaryMin"]); hi = float(row["salaryMax"])
            except (ValueError, TypeError):
                continue
            if lo <= 0 or hi <= 0 or hi < lo:
                continue
            mid = (lo + hi) / 2
            if mid < MIN_SALARY or mid > MAX_SALARY:
                continue
            buckets[(row["role_bucket"], row["seniority"])].append(mid)
    return buckets


def boot_median_ci(xs, n=BOOT):
    xs = np.array(xs)
    if len(xs) < 5:
        return (np.nan, np.nan)
    meds = []
    for _ in range(n):
        s = RNG.choice(xs, size=len(xs), replace=True)
        meds.append(np.median(s))
    return (np.percentile(meds, 2.5), np.percentile(meds, 97.5))


def rank_biserial(a, b):
    """Effect size for Mann-Whitney U."""
    u, _ = stats.mannwhitneyu(a, b, alternative="two-sided")
    return 1 - (2 * u) / (len(a) * len(b))


def main():
    buckets = load()
    print(f"{'role':4} {'level':7} {'N':>4} {'median':>8} {'p25':>8} {'p75':>8} {'CI_lo':>8} {'CI_hi':>8}")
    rows = []
    for role in ["DS", "MLE", "AIE"]:
        for lev in LEVEL_ORDER:
            xs = buckets[(role, lev)]
            if not xs:
                print(f"{role:4} {lev:7} {'0':>4}")
                rows.append([role, lev, 0, "", "", "", "", "", ""])
                continue
            xs_sorted = sorted(xs)
            med = np.median(xs_sorted)
            p25, p75 = np.percentile(xs_sorted, [25, 75])
            lo, hi = boot_median_ci(xs_sorted)
            mn = np.mean(xs_sorted)
            print(f"{role:4} {lev:7} {len(xs):>4} {med:>8,.0f} {p25:>8,.0f} {p75:>8,.0f} {lo:>8,.0f} {hi:>8,.0f}")
            rows.append([role, lev, len(xs), round(med), round(p25), round(p75), round(lo), round(hi), round(mn)])

    with open("phase_b_salary_by_level.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["role", "level", "N", "median", "p25", "p75", "ci_lo", "ci_hi", "mean"])
        w.writerows(rows)

    print("\nPairwise Mann-Whitney (adjacent levels):")
    print(f"{'role':4} {'transition':18} {'N_a':>4} {'N_b':>4} {'d_median':>10} {'rb_r':>6} {'p':>10}")
    pair_rows = []
    for role in ["DS", "MLE", "AIE"]:
        for a, b in [("entry", "mid"), ("mid", "senior"), ("senior", "staff")]:
            xa = buckets[(role, a)]; xb = buckets[(role, b)]
            if len(xa) < 10 or len(xb) < 10:
                print(f"{role:4} {a}->{b:11} {len(xa):>4} {len(xb):>4}   (too thin)")
                pair_rows.append([role, f"{a}->{b}", len(xa), len(xb), "", "", ""])
                continue
            d = np.median(xb) - np.median(xa)
            u, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            rb = rank_biserial(xa, xb)
            print(f"{role:4} {a}->{b:11} {len(xa):>4} {len(xb):>4} {d:>10,.0f} {rb:>6.2f} {p:>10.1e}")
            pair_rows.append([role, f"{a}->{b}", len(xa), len(xb), round(d), round(rb, 3), f"{p:.2e}"])

    with open("phase_b_pairwise.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["role", "transition", "N_a", "N_b", "delta_median", "rank_biserial_r", "p"])
        w.writerows(pair_rows)


if __name__ == "__main__":
    main()
