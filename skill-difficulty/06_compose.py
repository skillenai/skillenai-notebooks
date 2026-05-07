"""Compose the 5 signals into a per-skill difficulty index.

Reads:
  signal_seniority.csv         (gradient)
  signal_salary.csv            (coef in log-space)
  signal_supply_demand.csv     (sd_log10 — log10(blog_count_technical / job_count))
  signal_hhi.csv               (hhi — Herfindahl-Hirschman index)
  signal_idf.csv               (mean_idf_p50)

Z-scores each, blends equal-weight, writes:
  difficulty_index.csv  with raw + z + composite

For S/D we INVERT the sign so high = scarcer (more demand-heavy) = harder.
Skills missing from one signal get z=0 for that signal (treated as average).
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent


def load_csv(path, key="canonical_skill"):
    if not path.exists():
        return {}
    return {r[key]: r for r in csv.DictReader(open(path))}


def z(rows, col, invert=False):
    vals = [float(r[col]) for r in rows if r.get(col) not in (None, "", "0", "0.0")]
    if not vals:
        return [0.0] * len(rows)
    mu, sd = float(np.mean(vals)), float(np.std(vals)) or 1.0
    out = []
    for r in rows:
        v = r.get(col)
        if v in (None, ""):
            out.append(0.0); continue
        try:
            zv = (float(v) - mu) / sd
        except ValueError:
            zv = 0.0
        if invert:
            zv = -zv
        out.append(round(zv, 4))
    return out


def main():
    sen = load_csv(HERE / "signal_seniority.csv")
    sal = load_csv(HERE / "signal_salary.csv")
    sd  = load_csv(HERE / "signal_supply_demand.csv")
    hhi = load_csv(HERE / "signal_hhi.csv")
    idf = load_csv(HERE / "signal_idf.csv")

    universe = json.load(open(HERE / "canonical_universe.json"))
    all_skills = [s["name"] for s in universe["skills"]]

    rows = []
    for s in all_skills:
        rows.append({
            "canonical_skill":   s,
            "gradient":          sen.get(s, {}).get("gradient", ""),
            "salary_coef":       sal.get(s, {}).get("coef", ""),
            "sd_log10":          sd.get(s, {}).get("sd_log10", ""),
            "hhi":               hhi.get(s, {}).get("hhi", ""),
            "mean_idf":          idf.get(s, {}).get("mean_idf_p50", ""),
            "salary_n":          sal.get(s, {}).get("n_jobs_with_skill_in_sample", ""),
            "n_jobs_in_corpus":  hhi.get(s, {}).get("n_jobs", ""),
            "blog_count_tech":   sd.get(s, {}).get("blog_count_technical", ""),
        })

    rows_with = {
        "gradient_z":    z(rows, "gradient"),
        "salary_z":      z(rows, "salary_coef"),
        "sd_z":          z(rows, "sd_log10", invert=True),  # high = scarce
        "hhi_z":         z(rows, "hhi"),
        "idf_z":         z(rows, "mean_idf"),
    }
    for col, vals in rows_with.items():
        for r, v in zip(rows, vals):
            r[col] = v

    for r in rows:
        r["composite_z"] = round(
            (r["gradient_z"] + r["salary_z"] + r["sd_z"] + r["hhi_z"] + r["idf_z"]) / 5,
            4,
        )

    rows.sort(key=lambda r: -r["composite_z"])

    out_path = HERE / "difficulty_index.csv"
    fields = ["canonical_skill",
              "gradient", "salary_coef", "sd_log10", "hhi", "mean_idf",
              "gradient_z", "salary_z", "sd_z", "hhi_z", "idf_z",
              "composite_z",
              "salary_n", "n_jobs_in_corpus", "blog_count_tech"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} skills to {out_path.name}", file=sys.stderr)

    print("\nTop 25 hardest by composite (5 signals):", file=sys.stderr)
    for r in rows[:25]:
        print(f"  {r['canonical_skill']:30s} comp={r['composite_z']:+.2f}  "
              f"grad={r['gradient_z']:+.2f}  sal={r['salary_z']:+.2f}  "
              f"sd={r['sd_z']:+.2f}  hhi={r['hhi_z']:+.2f}  idf={r['idf_z']:+.2f}",
              file=sys.stderr)
    print("\nBottom 15 easiest:", file=sys.stderr)
    for r in rows[-15:]:
        print(f"  {r['canonical_skill']:30s} comp={r['composite_z']:+.2f}  "
              f"grad={r['gradient_z']:+.2f}  sal={r['salary_z']:+.2f}  "
              f"sd={r['sd_z']:+.2f}  hhi={r['hhi_z']:+.2f}  idf={r['idf_z']:+.2f}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
