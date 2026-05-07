"""Signal 2: Salary premium per skill via hedonic regression.

Model: log(midpoint_USD_salary) ~ role + locationCountry + seniorityLevel + skill_dummies

Uses scikit-learn Ridge with one-hot encoded categoricals + sparse skill matrix.
Drops skills with N(skill present) < 50 in the regression sample.

Per-skill coefficient = log-pp salary premium *holding role/country/seniority fixed*.
Higher = scarcer/harder skill (market-supply constrained).

Output: signal_salary.csv with
  canonical_skill, n_jobs_with_skill_in_sample, coef, coef_pct
"""
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).parent

MIN_SKILL_N = 30  # was 50; lowered after re-download tripled the USD sample.
                  # Below N=30 the Ridge estimates are too noisy for the
                  # regression to be useful as a comparison signal.
ALPHA = 1.0       # ridge regularization

# ML/AI roles + DE + general SWE for context — cap to a reasonable role universe
SUPPORTED_ROLES = None  # None = use all roles; we'll add light filtering


def load_data():
    universe = json.load(open(HERE / "canonical_universe.json"))
    skill_set = {s["name"] for s in universe["skills"]}

    rows = []
    with open(HERE / "jobs_usd_salary_canonical.csv") as f:
        for r in csv.DictReader(f):
            try:
                lo = float(r.get("salaryMin") or 0)
                hi = float(r.get("salaryMax") or 0)
            except ValueError:
                continue
            if lo <= 10000 or hi <= 10000 or lo > 1_000_000 or hi > 2_000_000:
                continue
            mid = (lo + hi) / 2 if hi > 0 else lo
            if mid < 30_000 or mid > 800_000:
                continue
            role = (r.get("role") or "").strip()
            sen = (r.get("seniorityLevel") or "").strip().lower() or "unknown"
            country = (r.get("locationCountry") or "").strip() or "Unknown"
            company = (r.get("companyCanonicalName") or "").strip()
            skills = [s for s in (r.get("canonical_skills") or "").split("|")
                      if s and s in skill_set]
            if not role:
                continue
            # Filter out extraction-artifact postings — empty
            # companyCanonicalName correlates with a templated 15-skill
            # boilerplate list that distorts coefficients (especially
            # 'inference' which jumps to a fake +48%).
            if not company:
                continue
            rows.append({
                "log_salary": math.log(mid),
                "role": role,
                "seniority": sen,
                "country": country,
                "skills": skills,
            })
    return rows, skill_set


def main():
    rows, skill_set = load_data()
    print(f"Regression rows: {len(rows)}", file=sys.stderr)

    # Build feature matrix
    skill_counts = Counter()
    for r in rows:
        for s in r["skills"]:
            skill_counts[s] += 1
    keep_skills = sorted([s for s, n in skill_counts.items() if n >= MIN_SKILL_N])
    print(f"Skills with N>={MIN_SKILL_N} in regression sample: {len(keep_skills)}",
          file=sys.stderr)

    skill_idx = {s: i for i, s in enumerate(keep_skills)}
    n = len(rows)

    # Skill sparse matrix (n × n_skills)
    data, ri, ci = [], [], []
    for i, r in enumerate(rows):
        for s in r["skills"]:
            j = skill_idx.get(s)
            if j is not None:
                ri.append(i); ci.append(j); data.append(1.0)
    X_skills = csr_matrix((data, (ri, ci)), shape=(n, len(keep_skills)))

    # Role + seniority + country one-hots (top-K to limit dim)
    role_top = [r for r, _ in Counter(x["role"] for x in rows).most_common(40)]
    sen_top = sorted(set(x["seniority"] for x in rows))
    country_top = [c for c, _ in Counter(x["country"] for x in rows).most_common(20)]
    role_top_set, country_top_set = set(role_top), set(country_top)

    cat_arr = np.array([
        [
            x["role"] if x["role"] in role_top_set else "OTHER",
            x["seniority"],
            x["country"] if x["country"] in country_top_set else "OTHER",
        ] for x in rows
    ])
    enc = OneHotEncoder(sparse_output=True, handle_unknown="ignore")
    X_cat = enc.fit_transform(cat_arr)
    cat_feat_names = enc.get_feature_names_out(["role", "seniority", "country"])

    X = hstack([X_cat, X_skills]).tocsr()
    y = np.array([r["log_salary"] for r in rows])
    print(f"Feature matrix: {X.shape}, target: {y.shape}", file=sys.stderr)

    model = Ridge(alpha=ALPHA, fit_intercept=True)
    model.fit(X, y)

    coefs = model.coef_
    n_cat = X_cat.shape[1]
    skill_coefs = coefs[n_cat:]
    print(f"R^2 in-sample: {model.score(X, y):.3f}", file=sys.stderr)

    out = []
    for s, j in skill_idx.items():
        coef = skill_coefs[j]
        out.append({
            "canonical_skill": s,
            "n_jobs_with_skill_in_sample": skill_counts[s],
            "coef": round(float(coef), 5),
            "coef_pct": round(float(math.exp(coef) - 1) * 100, 2),
        })
    out.sort(key=lambda r: -r["coef"])

    out_path = HERE / "signal_salary.csv"
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {len(out)} rows to {out_path.name}", file=sys.stderr)

    print("\nTop 20 highest premium:", file=sys.stderr)
    for r in out[:20]:
        print(f"  {r['canonical_skill']:35s} +{r['coef_pct']:+6.2f}%  N={r['n_jobs_with_skill_in_sample']:5d}",
              file=sys.stderr)
    print("\nBottom 20 lowest/negative premium:", file=sys.stderr)
    for r in out[-20:]:
        print(f"  {r['canonical_skill']:35s} {r['coef_pct']:+6.2f}%  N={r['n_jobs_with_skill_in_sample']:5d}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
