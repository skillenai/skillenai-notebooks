"""Compute Jaccard vs effort-weighted distance from Data Scientist to each role.

For each role, take its top-K skills (default K=30, like the prior post).
Skills are canonicalized.

Distance metrics from DS to target role:
  jaccard       = 1 - |DS ∩ T| / |DS ∪ T|              (raw skill set distance)
  unweighted_gap = |T \ DS|                             (count of skills to learn)
  effort_gap    = sum(composite_z(s)) for s in T \ DS   (weighted by difficulty)
                  shifted so min difficulty = 0, then summed; missing skills
                  default to 0 contribution.

Output: role_distance.csv with all metrics, plus markdown table for the report.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent

TOP_K = 30
DS_ROLE = "Data Scientist"

# Targets to compare. Some are aggregate roles defined in mle_split.json or
# combined in role_canon_skills.json.
TARGETS = [
    "Applied Scientist (no Amazon)",
    "Applied Scientist",
    "ML Engineer",
    "Applied/Research Wing",
    "MLE/Applied-Research-Training-Foundation",
    "MLE/Platform-Infrastructure-Inference",
    "AI Engineer",
    "Research Scientist",
    "Applied AI Engineer",
    "Research Engineer",
    "Applied ML Engineer",
]


def top_k_skills(role_skills, role, k=TOP_K):
    sk = role_skills.get(role, {})
    items = [(s, n) for s, n in sk.items() if not s.startswith("__") and n > 0]
    items.sort(key=lambda x: -x[1])
    return [s for s, _ in items[:k]]


def main():
    role_canon = json.load(open(HERE / "role_canon_skills.json"))
    diff = {}
    if (HERE / "difficulty_index.csv").exists():
        with open(HERE / "difficulty_index.csv") as f:
            for r in csv.DictReader(f):
                diff[r["canonical_skill"]] = float(r["composite_z"])

    if not diff:
        print("WARNING: difficulty_index.csv not found, will only compute Jaccard",
              file=sys.stderr)

    # Shift composite z so min in universe = 0 (so missing-skill contributions
    # are non-negative and effort_gap is monotonic in missing-skill count + difficulty)
    if diff:
        floor = min(diff.values())
        diff_shift = {s: v - floor for s, v in diff.items()}
    else:
        diff_shift = {}

    ds_skills = set(top_k_skills(role_canon, DS_ROLE))

    rows = []
    for tgt in TARGETS:
        if tgt not in role_canon:
            print(f"  skip (no data): {tgt}", file=sys.stderr)
            continue
        t_skills = set(top_k_skills(role_canon, tgt))

        union = ds_skills | t_skills
        intersect = ds_skills & t_skills
        jaccard = len(intersect) / len(union) if union else 0.0
        missing = t_skills - ds_skills

        unweighted_gap = len(missing)
        # Effort-gap: sum of (composite_z + shift) over missing skills
        effort_components = []
        for s in missing:
            v = diff_shift.get(s, 0.0)
            effort_components.append((s, v))
        effort_gap = sum(v for _, v in effort_components)
        # Average difficulty of the missing skills (interpretable: "how hard are they on avg")
        avg_diff = (effort_gap / unweighted_gap) if unweighted_gap > 0 else 0.0

        rows.append({
            "target_role": tgt,
            "n_overlap": len(intersect),
            "n_target_only": unweighted_gap,
            "n_ds_only": len(ds_skills - t_skills),
            "jaccard": round(jaccard, 4),
            "unweighted_gap": unweighted_gap,
            "effort_gap": round(effort_gap, 3),
            "avg_difficulty_of_missing": round(avg_diff, 3),
            "missing_skills_top10": "|".join(sorted(missing,
                                                    key=lambda s: -diff_shift.get(s, 0))[:10]),
        })

    # Sort by Jaccard ascending (longest paper-distance first, like the prior post's
    # Finding 1)
    rows.sort(key=lambda r: r["jaccard"])

    out_path = HERE / "role_distance.csv"
    fields = list(rows[0].keys())
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {len(rows)} rows to {out_path.name}", file=sys.stderr)

    print(f"\nDS top-{TOP_K} skills: {sorted(ds_skills)[:20]}...", file=sys.stderr)
    print("\n" + "="*100, file=sys.stderr)
    print(f"{'Target role':45s} {'Jaccard':>8s} {'Gap#':>5s} {'EffortGap':>10s} {'AvgDif':>8s}",
          file=sys.stderr)
    print("="*100, file=sys.stderr)
    # Re-sort by jaccard descending = shortest distance first for readability
    for r in sorted(rows, key=lambda r: -r["jaccard"]):
        print(f"{r['target_role']:45s} {r['jaccard']:>8.3f} "
              f"{r['unweighted_gap']:>5d} {r['effort_gap']:>10.2f} {r['avg_difficulty_of_missing']:>8.2f}",
              file=sys.stderr)
    print("\nMissing-skills detail (highest difficulty first):", file=sys.stderr)
    for r in rows:
        print(f"\n  {r['target_role']}: missing top-10 by difficulty:", file=sys.stderr)
        print(f"    {r['missing_skills_top10']}", file=sys.stderr)


if __name__ == "__main__":
    main()
