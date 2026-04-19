"""Generate visualizations for the skill-value-by-seniority analysis.

Plots:
  1. salary_by_level.png    — violin/box of salary by (role, level)
  2. skill_progression_<role>.png — heatmap of skill-share by seniority per role
  3. premium_comparison.png — dumbbell: C1 naive vs C2 hedonic premium for key skills
"""
import csv
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["font.family"] = "sans-serif"
sns.set_style("whitegrid")

LEVEL_ORDER = ["entry", "mid", "senior", "staff"]
LEVEL_LABELS = {"entry": "Entry", "mid": "Mid", "senior": "Senior", "staff": "Staff+"}
ROLE_LABELS = {"DS": "Data Scientist", "MLE": "ML Engineer", "AIE": "AI Engineer"}
MIN_SALARY = 30000
MAX_SALARY = 800000


# ----------------------------------------------------------------------------
# Plot 1: Salary by (role, level)
# ----------------------------------------------------------------------------
def plot_salary_by_level():
    df = pd.read_csv("jobs_merged.csv")
    df = df[df["salaryCurrency"] == "USD"]
    df = df[df["country"].astype(str).str.contains("US", na=False)]
    df["salaryMin"] = pd.to_numeric(df["salaryMin"], errors="coerce")
    df["salaryMax"] = pd.to_numeric(df["salaryMax"], errors="coerce")
    df = df.dropna(subset=["salaryMin", "salaryMax"])
    df = df[(df["salaryMin"] > 0) & (df["salaryMax"] >= df["salaryMin"])]
    df["salary"] = (df["salaryMin"] + df["salaryMax"]) / 2
    df = df[(df["salary"] >= MIN_SALARY) & (df["salary"] <= MAX_SALARY)]
    df["level_label"] = df["seniority"].map(LEVEL_LABELS)
    df["role_label"] = df["role_bucket"].map(ROLE_LABELS)
    df["salary_k"] = df["salary"] / 1000

    level_order = [LEVEL_LABELS[l] for l in LEVEL_ORDER]
    role_order = [ROLE_LABELS[r] for r in ["DS", "MLE", "AIE"]]

    fig, ax = plt.subplots(figsize=(11, 6))
    palette = {"Entry": "#C8E6C9", "Mid": "#81C784", "Senior": "#4CAF50", "Staff+": "#2E7D32"}
    sns.boxplot(
        data=df, x="role_label", y="salary_k", hue="level_label",
        order=role_order, hue_order=level_order, palette=palette,
        fliersize=2, width=0.75, ax=ax,
    )
    # Overlay medians as text
    for i, role in enumerate(role_order):
        for j, lev in enumerate(level_order):
            cell = df[(df["role_label"] == role) & (df["level_label"] == lev)]
            if len(cell) == 0:
                continue
            med = cell["salary_k"].median()
            n = len(cell)
            x = i + (j - 1.5) * 0.19
            ax.text(x, med + 4, f"${med:.0f}K", ha="center", va="bottom", fontsize=8, color="black")
            ax.text(x, 40, f"n={n}", ha="center", va="bottom", fontsize=7, color="#666")

    ax.set_ylabel("Salary midpoint (USD, thousands)")
    ax.set_xlabel("")
    ax.set_title("Salary distribution by role and seniority (US postings, USD)", fontsize=12)
    ax.legend(title="Seniority", loc="upper left", frameon=True)
    ax.set_ylim(30, 450)
    plt.tight_layout()
    plt.savefig("salary_by_level.png", bbox_inches="tight")
    plt.close()
    print("Wrote salary_by_level.png")


# ----------------------------------------------------------------------------
# Plot 2: skill progression heatmap per role
# ----------------------------------------------------------------------------
def plot_skill_progression(role, top_n=20):
    df = pd.read_csv(f"phase_a_{role.lower()}_skills_by_seniority.csv")
    # Pick top-N skills by a "level-up spread" criterion: max |resid - mean| across levels
    resid_cols = ["resid_entry", "resid_mid", "resid_senior", "resid_staff"]
    df["spread"] = df[resid_cols].max(axis=1) - df[resid_cols].min(axis=1)
    # Also require decent omnibus significance or a meaningful shift
    picked = df.sort_values("spread", ascending=False).head(top_n).copy()
    # Sort by monotonic trend: staff residual - entry residual
    picked["trend"] = picked["resid_staff"] - picked["resid_entry"]
    picked = picked.sort_values("trend", ascending=False)

    mat = picked[["entry_pct", "mid_pct", "senior_pct", "staff_pct"]].values
    labels = picked["skill"].tolist()

    fig, ax = plt.subplots(figsize=(9, max(4, 0.3 * len(labels) + 1)))
    sns.heatmap(
        mat, annot=True, fmt=".0f", cmap="RdYlGn",
        xticklabels=[LEVEL_LABELS[l] for l in LEVEL_ORDER],
        yticklabels=labels,
        cbar_kws={"label": "% of jobs requiring skill"},
        linewidths=0.4, linecolor="white", ax=ax, vmin=0,
    )
    ax.set_title(f"{ROLE_LABELS[role]}: skill demand by seniority (top {len(labels)} by change)", fontsize=11)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(f"skill_progression_{role.lower()}.png", bbox_inches="tight")
    plt.close()
    print(f"Wrote skill_progression_{role.lower()}.png")


# ----------------------------------------------------------------------------
# Plot 3: C1 (naive) vs C2 (hedonic) premium dumbbell
# ----------------------------------------------------------------------------
def plot_premium_comparison():
    c1 = pd.read_csv("phase_c1_pooled.csv")
    c2 = pd.read_csv("phase_c2_pooled.csv")
    c1 = c1.rename(columns={"premium_pct": "c1_pct", "premium_vs_baseline": "c1_dollar", "n": "c1_n"})
    c2 = c2.rename(columns={"premium_pct": "c2_pct", "premium_dollar": "c2_dollar", "n": "c2_n"})

    df = c1.merge(c2, on="skill", how="inner")
    df = df[(df["c1_n"] >= 25) & (df["c2_n"] >= 25)]
    # Rank by absolute c2 premium; keep top 12 positive + bottom 8 negative
    df = df.sort_values("c2_dollar", ascending=False)
    top = df.head(12)
    bot = df.tail(8)
    show = pd.concat([top, bot]).drop_duplicates(subset=["skill"]).reset_index(drop=True)
    show = show.sort_values("c2_dollar", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, max(5, 0.35 * len(show) + 1)))
    y = np.arange(len(show))
    ax.hlines(y, show["c1_dollar"], show["c2_dollar"], color="#999", alpha=0.5, zorder=1)
    ax.scatter(show["c1_dollar"], y, label="C1 naive median premium", color="#FFC107", s=70, zorder=3, edgecolor="white")
    ax.scatter(show["c2_dollar"], y, label="C2 hedonic premium (controls role+seniority)", color="#1976D2", s=70, zorder=3, edgecolor="white")
    ax.axvline(0, color="black", lw=0.8, alpha=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(show["skill"])
    ax.set_xlabel("Salary premium vs baseline (USD)")
    ax.set_title("Naive skill-salary ranking vs controlled premium (pooled DS+MLE+AIE)", fontsize=11)
    ax.legend(loc="lower right", frameon=True)
    ax.grid(axis="x", alpha=0.3)
    ax.grid(axis="y", alpha=0)

    # Annotate differences
    for i, row in show.iterrows():
        d = row["c2_dollar"] - row["c1_dollar"]
        x = max(row["c1_dollar"], row["c2_dollar"]) + 1500
        ax.text(x, i, f"Δ ${d:+,.0f}", va="center", fontsize=8, color="#444")

    # xlim padding
    left = min(show["c1_dollar"].min(), show["c2_dollar"].min()) - 5000
    right = max(show["c1_dollar"].max(), show["c2_dollar"].max()) + 25000
    ax.set_xlim(left, right)
    plt.tight_layout()
    plt.savefig("premium_comparison.png", bbox_inches="tight")
    plt.close()
    print("Wrote premium_comparison.png")


# ----------------------------------------------------------------------------
# Plot 4: Per-role hedonic premium top/bottom
# ----------------------------------------------------------------------------
def plot_role_premium(role):
    df = pd.read_csv(f"phase_c2_{role.lower()}.csv")
    df = df[df["n"] >= 20]
    df = df.sort_values("premium_dollar", ascending=True)
    top = df.tail(10)
    bot = df.head(8)
    show = pd.concat([bot, top]).drop_duplicates(subset=["skill"]).reset_index(drop=True)
    show = show.sort_values("premium_dollar", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(9, max(4, 0.32 * len(show) + 1)))
    colors = ["#D32F2F" if d < 0 else "#388E3C" for d in show["premium_dollar"]]
    y = np.arange(len(show))
    ax.barh(y, show["premium_dollar"], color=colors, alpha=0.85)
    ax.errorbar(
        show["premium_dollar"], y,
        xerr=[show["premium_dollar"] - show["dollar_ci_lo"], show["dollar_ci_hi"] - show["premium_dollar"]],
        fmt="none", ecolor="black", alpha=0.5, capsize=3, lw=0.8,
    )
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(show["skill"])
    ax.set_xlabel("Salary premium (USD, vs median) holding seniority fixed")
    ax.set_title(f"{ROLE_LABELS[role]}: skill-level salary premiums (hedonic, 95% CI)", fontsize=11)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"premium_{role.lower()}.png", bbox_inches="tight")
    plt.close()
    print(f"Wrote premium_{role.lower()}.png")


if __name__ == "__main__":
    plot_salary_by_level()
    for r in ["DS", "MLE", "AIE"]:
        plot_skill_progression(r)
    plot_premium_comparison()
    for r in ["DS", "MLE"]:
        plot_role_premium(r)
    print("All plots written.")
