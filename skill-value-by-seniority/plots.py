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
def plot_skill_progression(role, top_n=24):
    df = pd.read_csv(f"phase_a_{role.lower()}_skills_by_seniority.csv")
    resid_cols = ["resid_entry", "resid_mid", "resid_senior", "resid_staff"]
    pct_cols = ["entry_pct", "mid_pct", "senior_pct", "staff_pct"]

    df["spread"] = df[resid_cols].max(axis=1) - df[resid_cols].min(axis=1)
    picked = df.sort_values("spread", ascending=False).head(top_n).copy()

    # Classify each picked skill as climbing / dropping / mid-peaking
    def classify(row):
        peak_idx = int(np.argmax([row[c] for c in pct_cols]))
        peak = row[pct_cols[peak_idx]]
        entry, mid, senior, staff = row[pct_cols[0]], row[pct_cols[1]], row[pct_cols[2]], row[pct_cols[3]]
        if peak_idx == 3 and staff > entry + 1:
            return ("climbing", 0)  # peak at staff
        if peak_idx == 0 and entry > staff + 1:
            return ("dropping", 2)  # peak at entry
        if peak_idx in (1, 2) and entry < peak - 1 and staff < peak - 1:
            return ("mid-peaking", 1)  # peak at mid or senior
        # monotonic increasing (peak at staff) or decreasing captured above; remainder = ambiguous
        return ("other", 3)

    picked[["shape", "order"]] = picked.apply(lambda r: pd.Series(classify(r)), axis=1)
    # Sort: climbing first, then mid-peaking, then dropping, then other. Within each, by peak level then spread.
    picked["peak_idx"] = picked[pct_cols].values.argmax(axis=1)
    picked = picked.sort_values(["order", "peak_idx", "spread"], ascending=[True, True, False]).reset_index(drop=True)

    mat = picked[pct_cols].values
    labels = picked["skill"].tolist()

    # Row-normalize: each row scales to [0, 1] for color; keep raw pct as annotation.
    row_max = mat.max(axis=1, keepdims=True)
    row_min = mat.min(axis=1, keepdims=True)
    span = np.where(row_max > row_min, row_max - row_min, 1)
    mat_norm = (mat - row_min) / span

    SHAPE_COLORS = {"climbing": "#2E7D32", "mid-peaking": "#F9A825", "dropping": "#C62828", "other": "#BDBDBD"}
    # Prefix each label with a shape glyph
    SHAPE_GLYPH = {"climbing": "^", "mid-peaking": "~", "dropping": "v", "other": "-"}
    prefixed_labels = [f"{SHAPE_GLYPH[s]}  {lbl}" for s, lbl in zip(picked["shape"], labels)]

    fig, ax = plt.subplots(figsize=(10.5, max(5, 0.34 * len(labels) + 1.6)))
    sns.heatmap(
        mat_norm, annot=mat, fmt=".0f", cmap="RdYlGn",
        xticklabels=[LEVEL_LABELS[l] for l in LEVEL_ORDER],
        yticklabels=prefixed_labels,
        cbar=False,
        linewidths=0.4, linecolor="white", ax=ax, vmin=0, vmax=1,
    )

    # Color the glyph in each y-tick label by shape
    for tick, shape in zip(ax.get_yticklabels(), picked["shape"]):
        # Replace the label with a RichText-free two-color workaround: use the shape color for the entire tick.
        tick.set_color(SHAPE_COLORS[shape])

    from matplotlib.patches import Patch
    handles = [
        Patch(color=SHAPE_COLORS["climbing"], label="^  Climbing (peak at Staff+)"),
        Patch(color=SHAPE_COLORS["mid-peaking"], label="~  Mid-peaking (peak at Mid/Senior)"),
        Patch(color=SHAPE_COLORS["dropping"], label="v  Dropping (peak at Entry)"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.04),
              frameon=False, fontsize=9, ncol=3)

    ax.set_title(f"{ROLE_LABELS[role]}: skill demand by seniority (color normalized per row; value = % of jobs)", fontsize=10.5)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=9.5)
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
