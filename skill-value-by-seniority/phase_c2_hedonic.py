"""Phase C2: Hedonic regression to quantify skill-level salary premiums holding controls fixed.

Model:  log(salary_midpoint) ~ role + seniority + skill_dummies
        (US-only, USD-only; salary midpoint = (min+max)/2)

Procedure:
  1. Lasso with cross-validated alpha to select skills with non-zero coefficients
  2. OLS refit on selected skills (+ all controls) for interpretable CIs
  3. Report dollar premium at each role's median salary
  4. Run pooled model (all 3 roles) + per-role for DS and MLE (AIE too thin)
"""
import csv
import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from collections import Counter

CSV_IN = "jobs_merged.csv"
MIN_SALARY = 30000
MAX_SALARY = 800000
MIN_SKILL_JOBS = 20
SEED = 42


def load():
    df = pd.read_csv(CSV_IN)
    df = df[df["salaryCurrency"] == "USD"]
    df = df[df["country"].str.contains("US", na=False)]
    df["salaryMin"] = pd.to_numeric(df["salaryMin"], errors="coerce")
    df["salaryMax"] = pd.to_numeric(df["salaryMax"], errors="coerce")
    df = df.dropna(subset=["salaryMin", "salaryMax"])
    df = df[(df["salaryMin"] > 0) & (df["salaryMax"] >= df["salaryMin"])]
    df["salary"] = (df["salaryMin"] + df["salaryMax"]) / 2
    df = df[(df["salary"] >= MIN_SALARY) & (df["salary"] <= MAX_SALARY)]
    df["log_salary"] = np.log(df["salary"])
    df["skill_list"] = df["skills"].fillna("").str.split("|").apply(lambda xs: [s for s in xs if s])
    df = df.reset_index(drop=True)
    return df


def build_skill_matrix(df, min_n=MIN_SKILL_JOBS):
    cnt = Counter()
    for sk in df["skill_list"]:
        cnt.update(sk)
    skills = sorted([s for s, c in cnt.items() if c >= min_n])
    X = np.zeros((len(df), len(skills)), dtype=int)
    for i, sk in enumerate(df["skill_list"]):
        for s in sk:
            if s in skills:
                X[i, skills.index(s)] = 1
    return X, skills


def lasso_select(X_skills, X_ctrl, y, skills):
    """Scale + LassoCV. Returns list of skill names with non-zero coefs."""
    X = np.hstack([X_ctrl, X_skills])
    scaler = StandardScaler(with_mean=False)  # keep sparsity
    X_s = scaler.fit_transform(X)
    las = LassoCV(cv=5, random_state=SEED, max_iter=20000, n_alphas=50).fit(X_s, y)
    n_ctrl = X_ctrl.shape[1]
    coefs = las.coef_[n_ctrl:]
    selected = [s for s, c in zip(skills, coefs) if abs(c) > 1e-6]
    return selected, las


def fit_ols(df, skills, controls_onehot, label, median_salary):
    # Build design matrix: intercept + controls + skills
    skill_cols = {f"skill__{s}": [(s in sk) for sk in df["skill_list"]] for s in skills}
    Xd = pd.concat([controls_onehot.reset_index(drop=True),
                    pd.DataFrame(skill_cols)], axis=1).astype(float)
    Xd = sm.add_constant(Xd)
    y = df["log_salary"].values
    try:
        model = sm.OLS(y, Xd).fit(cov_type="HC3")
    except Exception as e:
        print(f"OLS failed for {label}: {e}")
        return None, None

    rows = []
    for name in Xd.columns:
        if not name.startswith("skill__"):
            continue
        coef = model.params[name]
        pval = model.pvalues[name]
        ci_lo, ci_hi = model.conf_int().loc[name]
        # dollar premium at this role's median
        dollar = median_salary * (np.exp(coef) - 1)
        dollar_lo = median_salary * (np.exp(ci_lo) - 1)
        dollar_hi = median_salary * (np.exp(ci_hi) - 1)
        n = int(pd.Series(Xd[name]).sum())
        rows.append({
            "skill": name.replace("skill__", ""),
            "n": n,
            "coef_log": round(coef, 4),
            "premium_pct": round(100 * (np.exp(coef) - 1), 1),
            "premium_dollar": round(dollar),
            "dollar_ci_lo": round(dollar_lo),
            "dollar_ci_hi": round(dollar_hi),
            "p_value": pval,
        })
    rows.sort(key=lambda r: -r["premium_dollar"])
    return rows, model


def run(df, label, out_csv, include_role=True):
    print(f"\n=== {label} (N={len(df)}) ===")
    median_salary = df["salary"].median()
    print(f"Baseline median: ${median_salary:,.0f}")

    # Controls: role + seniority (+ role if pooled)
    ctrl_cols = []
    if include_role:
        role_d = pd.get_dummies(df["role_bucket"], prefix="role", drop_first=True).astype(int)
        ctrl_cols.append(role_d)
    sen_d = pd.get_dummies(df["seniority"], prefix="sen", drop_first=True).astype(int)
    ctrl_cols.append(sen_d)
    controls_onehot = pd.concat(ctrl_cols, axis=1)
    X_ctrl = controls_onehot.values.astype(float)
    y = df["log_salary"].values

    # Build skill matrix
    X_skills, skills = build_skill_matrix(df)
    print(f"Candidate skills (>= {MIN_SKILL_JOBS} jobs): {len(skills)}")

    # Lasso selection
    selected, las = lasso_select(X_skills, X_ctrl, y, skills)
    print(f"Lasso selected {len(selected)}/{len(skills)} skills (alpha={las.alpha_:.4f})")

    # OLS refit
    rows, model = fit_ols(df, selected, controls_onehot, label, median_salary)
    if rows is None:
        return

    # Print top/bottom
    print(f"\nOLS R^2 = {model.rsquared:.3f}  adj R^2 = {model.rsquared_adj:.3f}")
    # Show control coefficients
    print("\nControl coefficients (log-points; exp(coef)-1 = % premium):")
    for name in model.params.index:
        if name == "const" or name.startswith("skill__"):
            continue
        p = model.params[name]
        pv = model.pvalues[name]
        print(f"  {name:20} {p:+.3f}  ({(np.exp(p)-1)*100:+.1f}%)  p={pv:.2e}")

    print(f"\nTop 20 skills by dollar premium:")
    print(f"{'skill':30} {'N':>4} {'prem%':>6} {'prem$':>8} {'CI_lo':>8} {'CI_hi':>8} {'p':>9}")
    for r in rows[:20]:
        print(f"{r['skill'][:30]:30} {r['n']:>4} {r['premium_pct']:>+5.1f}% ${r['premium_dollar']:>+7,} ${r['dollar_ci_lo']:>+6,} ${r['dollar_ci_hi']:>+6,} {r['p_value']:>8.2e}")
    print(f"\nBottom 10 (discount):")
    for r in rows[-10:]:
        print(f"{r['skill'][:30]:30} {r['n']:>4} {r['premium_pct']:>+5.1f}% ${r['premium_dollar']:>+7,} ${r['dollar_ci_lo']:>+6,} ${r['dollar_ci_hi']:>+6,} {r['p_value']:>8.2e}")

    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out_csv}")


def main():
    df = load()
    print(f"Total salaried US+USD jobs: {len(df)}")
    run(df, "POOLED (DS+MLE+AIE)", "phase_c2_pooled.csv", include_role=True)
    run(df[df["role_bucket"] == "DS"].reset_index(drop=True), "DS only", "phase_c2_ds.csv", include_role=False)
    run(df[df["role_bucket"] == "MLE"].reset_index(drop=True), "MLE only", "phase_c2_mle.csv", include_role=False)


if __name__ == "__main__":
    main()
