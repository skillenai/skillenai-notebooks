"""Phase A: skill proportions x seniority for DS/MLE/AIE.

Per role:
  - Contingency table: skills x seniority levels (entry/mid/senior/staff)
  - Omnibus chi-square test
  - Per-skill 4x2 chi-square + standardized residuals vs Bonferroni threshold
  - Pairwise mid->senior and senior->staff comparisons to identify "level-up" skills
  - Output: CSVs + markdown tables
"""
import csv
import sys
from collections import Counter, defaultdict
import numpy as np
from scipy import stats

CSV_IN = "jobs_merged.csv"
LEVEL_ORDER = ["entry", "mid", "senior", "staff"]
MIN_SKILL_JOBS = 40  # skill must appear in >= this many jobs within the role to be tested
TOP_N = 40  # top skills per role for main tables


def load():
    by_role = defaultdict(list)  # role -> list of (seniority, skills_set)
    with open(CSV_IN) as f:
        for row in csv.DictReader(f):
            role = row["role_bucket"]
            sen = row["seniority"]
            skills = set(s for s in (row["skills"] or "").split("|") if s)
            by_role[role].append((sen, skills))
    return by_role


def contingency(data, skill, levels):
    """Build a 2x4 table: rows = [has_skill, no_skill], cols = levels. Counts."""
    table = np.zeros((2, len(levels)), dtype=int)
    for i, lev in enumerate(levels):
        for sen, sk in data:
            if sen != lev:
                continue
            if skill in sk:
                table[0, i] += 1
            else:
                table[1, i] += 1
    return table


def analyze_role(role, rows, out_prefix):
    print(f"\n=== {role} (N={len(rows)}) ===")
    level_counts = Counter(s for s, _ in rows)
    print("Level N:", {l: level_counts[l] for l in LEVEL_ORDER})

    # Candidate skills: appear in >= MIN_SKILL_JOBS jobs across the role
    skill_totals = Counter()
    for _, sk in rows:
        skill_totals.update(sk)
    candidates = [s for s, c in skill_totals.items() if c >= MIN_SKILL_JOBS]
    print(f"Skills tested: {len(candidates)} (min jobs = {MIN_SKILL_JOBS})")

    results = []
    bonf = 0.05 / max(1, len(candidates))

    for skill in candidates:
        tab = contingency(rows, skill, LEVEL_ORDER)
        # Omnibus 2x4 chi-square
        try:
            chi2, p, dof, exp = stats.chi2_contingency(tab)
        except ValueError:
            continue

        # Row proportions of has_skill at each level
        level_n = tab.sum(axis=0)
        props = np.where(level_n > 0, tab[0] / level_n, 0)

        # Pearson standardized residuals (observed - expected) / sqrt(expected * (1-row_prop) * (1-col_prop))
        with np.errstate(divide="ignore", invalid="ignore"):
            row_totals = tab.sum(axis=1, keepdims=True)
            col_totals = tab.sum(axis=0, keepdims=True)
            n = tab.sum()
            std_resid = (tab - exp) / np.sqrt(
                exp * (1 - row_totals / n) * (1 - col_totals / n)
            )
        resid_has = std_resid[0]  # residuals for "has_skill" row

        # Pairwise mid vs senior, senior vs staff: 2x2 chi-square on "has_skill" counts
        def pairwise(a, b):
            t = np.array([[tab[0, a], tab[0, b]], [tab[1, a], tab[1, b]]])
            if t.sum(axis=0).min() < 10:
                return (np.nan, np.nan, props[b] - props[a])
            try:
                c2, pp, _, _ = stats.chi2_contingency(t)
                return (c2, pp, props[b] - props[a])
            except ValueError:
                return (np.nan, np.nan, props[b] - props[a])

        c2_ms, p_ms, d_ms = pairwise(1, 2)  # mid -> senior
        c2_ss, p_ss, d_ss = pairwise(2, 3)  # senior -> staff
        c2_em, p_em, d_em = pairwise(0, 1)  # entry -> mid

        results.append({
            "skill": skill,
            "total": skill_totals[skill],
            "entry_pct": props[0] * 100,
            "mid_pct": props[1] * 100,
            "senior_pct": props[2] * 100,
            "staff_pct": props[3] * 100,
            "entry_n": int(tab[0, 0]),
            "mid_n": int(tab[0, 1]),
            "senior_n": int(tab[0, 2]),
            "staff_n": int(tab[0, 3]),
            "omnibus_chi2": chi2,
            "omnibus_p": p,
            "omnibus_sig": p < bonf,
            "resid_entry": resid_has[0],
            "resid_mid": resid_has[1],
            "resid_senior": resid_has[2],
            "resid_staff": resid_has[3],
            "delta_entry_to_mid": d_em * 100,
            "delta_mid_to_senior": d_ms * 100,
            "delta_senior_to_staff": d_ss * 100,
            "p_mid_to_senior": p_ms,
            "p_senior_to_staff": p_ss,
            "p_entry_to_mid": p_em,
            # Level-up score: combined std residual change across transitions, signed
            "level_up_score": resid_has[3] - resid_has[0],
        })

    results.sort(key=lambda r: -r["total"])
    # Write full CSV
    out_csv = f"{out_prefix}_{role.lower()}_skills_by_seniority.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"Wrote {len(results)} skills -> {out_csv}")
    print(f"Bonferroni threshold: {bonf:.2e}")
    return results, bonf, level_counts


def markdown_tables(role, results, bonf, level_counts, fh):
    fh.write(f"\n## {role} (N = {sum(level_counts.values())})\n\n")
    fh.write(f"Levels: entry={level_counts['entry']}, mid={level_counts['mid']}, senior={level_counts['senior']}, staff+={level_counts['staff']}. Bonferroni p<{bonf:.2e} for omnibus.\n\n")

    # Table 1: Top skills with level progression
    top = results[:TOP_N]
    fh.write("### Top skills: share-of-jobs by seniority\n\n")
    fh.write("| Skill | Entry | Mid | Senior | Staff+ | Omnibus p | Level-up \u0394 |\n")
    fh.write("|---|---:|---:|---:|---:|---:|---:|\n")
    for r in top:
        sig = "**" if r["omnibus_sig"] else ""
        fh.write(f"| {r['skill']} | {r['entry_pct']:.0f}% | {r['mid_pct']:.0f}% | {r['senior_pct']:.0f}% | {r['staff_pct']:.0f}% | {sig}{r['omnibus_p']:.1e}{sig} | {r['level_up_score']:+.2f} |\n")

    # Table 2: Skills that separate MID from SENIOR (the key transition)
    fh.write("\n### Skills that most separate Mid from Senior\n\n")
    ms_sig = [r for r in results if r["p_mid_to_senior"] is not None and not np.isnan(r["p_mid_to_senior"]) and r["p_mid_to_senior"] < bonf]
    ms_sig.sort(key=lambda r: -abs(r["delta_mid_to_senior"]))
    fh.write("| Skill | Mid % | Senior % | \u0394 | p |\n|---|---:|---:|---:|---:|\n")
    for r in ms_sig[:15]:
        fh.write(f"| {r['skill']} | {r['mid_pct']:.0f}% | {r['senior_pct']:.0f}% | {r['delta_mid_to_senior']:+.1f} pp | {r['p_mid_to_senior']:.1e} |\n")

    # Table 3: Skills that separate SENIOR from STAFF
    fh.write("\n### Skills that most separate Senior from Staff+\n\n")
    ss_sig = [r for r in results if r["p_senior_to_staff"] is not None and not np.isnan(r["p_senior_to_staff"]) and r["p_senior_to_staff"] < bonf]
    ss_sig.sort(key=lambda r: -abs(r["delta_senior_to_staff"]))
    fh.write("| Skill | Senior % | Staff+ % | \u0394 | p |\n|---|---:|---:|---:|---:|\n")
    for r in ss_sig[:15]:
        fh.write(f"| {r['skill']} | {r['senior_pct']:.0f}% | {r['staff_pct']:.0f}% | {r['delta_senior_to_staff']:+.1f} pp | {r['p_senior_to_staff']:.1e} |\n")

    # Table 4: Entry-level signature skills (high at entry, drops with level)
    fh.write("\n### Entry-level signature skills (Entry > Mid, drops with level)\n\n")
    entry_sig = [r for r in results if r["resid_entry"] > 2 and r["delta_entry_to_mid"] < 0]
    entry_sig.sort(key=lambda r: -r["resid_entry"])
    fh.write("| Skill | Entry % | Mid % | Senior % | Staff+ % | Entry residual |\n|---|---:|---:|---:|---:|---:|\n")
    for r in entry_sig[:10]:
        fh.write(f"| {r['skill']} | {r['entry_pct']:.0f}% | {r['mid_pct']:.0f}% | {r['senior_pct']:.0f}% | {r['staff_pct']:.0f}% | {r['resid_entry']:+.2f} |\n")


def main():
    by_role = load()
    with open("phase_a_tables.md", "w") as fh:
        fh.write("# Phase A: Skill proportions by seniority\n")
        fh.write("\nShare of jobs requiring each skill. Omnibus = 2x4 chi-square (has_skill across 4 levels). Bonferroni-corrected. \u0394 = percentage-point change between levels. Level-up \u0394 = staff residual minus entry residual (positive = accumulates with seniority).\n")
        for role in ["DS", "MLE", "AIE"]:
            rows = by_role[role]
            results, bonf, lc = analyze_role(role, rows, "phase_a")
            markdown_tables(role, results, bonf, lc, fh)
    print("\nWrote phase_a_tables.md")


if __name__ == "__main__":
    main()
