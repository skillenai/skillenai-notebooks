"""Generate the report charts:

  01_jaccard_vs_effort.png — scatter, role-distance ranks side by side
  02_difficulty_breakdown.png — for the missing skills in DS->{AIE, MLE-Platform},
      stacked bar showing the four signal contributions per skill
  03_skill_difficulty_landscape.png — 2D scatter of all skills (gradient vs scholarly_ratio)
      colored by salary_coef, sized by depth, with key labels
  04_distance_rank_swap.png — bump-chart: each role's rank by Jaccard vs by effort
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def chart_jaccard_vs_effort():
    rows = load_csv(HERE / "role_distance.csv")
    rows.sort(key=lambda r: float(r["jaccard"]))

    labels = [r["target_role"] for r in rows]
    jacc = [float(r["jaccard"]) for r in rows]
    eff = [float(r["effort_gap"]) for r in rows]
    gap_n = [int(r["unweighted_gap"]) for r in rows]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    y = np.arange(len(labels))
    # Left: Jaccard distance (1-jaccard so bar grows with distance)
    ax1.barh(y, [1 - j for j in jacc], color="#4c78a8")
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels)
    ax1.invert_yaxis()
    ax1.set_xlabel("1 − Jaccard  (paper distance)")
    ax1.set_title("By Jaccard distance from Data Scientist", fontweight="bold")
    for i, (j, n) in enumerate(zip(jacc, gap_n)):
        ax1.text(1 - j + 0.005, i, f"  J={j:.3f}  ({n} skills)", va="center", fontsize=9)

    # Right: effort gap, ordered same as left for visual diff
    ax2.barh(y, eff, color="#d62728")
    ax2.set_yticks(y); ax2.set_yticklabels([])  # share labels
    ax2.invert_yaxis()
    ax2.set_xlabel("Effort gap (Σ difficulty of missing skills)")
    ax2.set_title("By effort gap from Data Scientist", fontweight="bold")
    for i, e in enumerate(eff):
        ax2.text(e + 0.05, i, f"  {e:.1f}", va="center", fontsize=9)

    fig.suptitle("Data Scientist → target role: paper distance vs effort distance",
                 fontweight="bold", fontsize=13)
    plt.tight_layout()
    out = HERE / "01_jaccard_vs_effort.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


def chart_distance_rank_swap():
    rows = load_csv(HERE / "role_distance.csv")
    n = len(rows)
    by_jacc = sorted(rows, key=lambda r: float(r["jaccard"]))   # ascending: lower Jaccard = farther
    by_eff = sorted(rows, key=lambda r: -float(r["effort_gap"]))  # descending: higher effort = harder

    rank_jacc = {r["target_role"]: i + 1 for i, r in enumerate(by_jacc)}
    rank_eff = {r["target_role"]: i + 1 for i, r in enumerate(by_eff)}

    fig, ax = plt.subplots(figsize=(10, 0.45 * n + 2))
    for r in rows:
        role = r["target_role"]
        a = rank_jacc[role]
        b = rank_eff[role]
        # Color: red if effort moves it harder, green if easier
        delta = a - b
        color = "#2ca02c" if delta > 0 else "#d62728" if delta < 0 else "#7f7f7f"
        ax.plot([1, 2], [a, b], color=color, marker="o", linewidth=2, markersize=8)
        ax.text(0.95, a, role, ha="right", va="center", fontsize=10)
        ax.text(2.05, b, f"  {role}", ha="left", va="center", fontsize=10)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Rank by Jaccard\n(longer paper distance → harder rank)",
                        "Rank by effort\n(higher effort gap → harder rank)"])
    ax.invert_yaxis()
    ax.set_ylim(n + 0.5, 0.5)
    ax.set_xlim(-1, 4)
    ax.set_yticks([])
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.set_title("Rank swap: paper distance vs effort gap from Data Scientist",
                 fontweight="bold")
    plt.tight_layout()
    out = HERE / "04_distance_rank_swap.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


def chart_skill_landscape():
    diff = load_csv(HERE / "difficulty_index.csv")

    # Filter to skills with complete signals
    pts = []
    for r in diff:
        try:
            grad_z = float(r["gradient_z"])
            idf_z  = float(r["idf_z"])
            sal_z  = float(r["salary_z"])
            hhi_z  = float(r["hhi_z"])
        except (ValueError, KeyError):
            continue
        if r.get("gradient") and r.get("mean_idf"):
            pts.append({
                "skill": r["canonical_skill"],
                "x": float(r["gradient"]),
                "y": float(r["mean_idf"]),
                "color": float(r["salary_coef"] or 0),
                "size": (float(r["hhi"]) if r.get("hhi") else 0.005) * 600 + 30,
            })

    fig, ax = plt.subplots(figsize=(13, 9))
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    cs = [p["color"] for p in pts]
    ss = [p["size"] for p in pts]

    sc = ax.scatter(xs, ys, c=cs, s=ss, cmap="RdYlBu_r", alpha=0.7,
                    edgecolors="white", linewidths=0.5)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Salary premium coefficient (log-pp)")

    # Label salient skills
    LABEL = {"kubernetes", "terraform", "docker", "fine-tuning", "rag", "transformer",
             "rlhf", "distributed training", "machine learning", "python", "sql", "react",
             "javascript", "git", "pytorch", "tensorflow", "pandas", "agentic workflows",
             "prompt engineering", "langchain", "llms", "sft", "dpo", "computer vision",
             "reinforcement learning", "cuda", "deep learning", "vector databases",
             "evaluation", "experimentation", "a/b testing", "causal inference"}
    for p in pts:
        if p["skill"] in LABEL:
            ax.annotate(p["skill"], (p["x"], p["y"]),
                        xytext=(5, 4), textcoords="offset points", fontsize=9, alpha=0.8)

    ax.set_xlabel("Seniority gradient  (lower → entry-friendly,  higher → senior-skewed)")
    ax.set_ylabel("Vocabulary jargon (mean per-doc IDF in technical-blog corpus)")
    ax.set_title("Skill difficulty landscape\n"
                 "Color = salary premium  ·  Size = employer concentration (HHI)",
                 fontweight="bold")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    out = HERE / "03_skill_difficulty_landscape.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.name}  ({len(pts)} skills plotted)", file=sys.stderr)


def chart_difficulty_breakdown():
    diff = {r["canonical_skill"]: r for r in load_csv(HERE / "difficulty_index.csv")}
    rd = load_csv(HERE / "role_distance.csv")
    role_canon = json.load(open(HERE / "role_canon_skills.json"))

    targets = ["AI Engineer", "Applied AI Engineer",
               "MLE/Platform-Infrastructure-Inference",
               "MLE/Applied-Research-Training-Foundation",
               "Applied Scientist (no Amazon)"]
    targets = [t for t in targets if t in role_canon]

    fig, axes = plt.subplots(len(targets), 1, figsize=(13, 2.2 * len(targets)),
                              sharex=False)
    if len(targets) == 1:
        axes = [axes]

    for ax, tgt in zip(axes, targets):
        # Top-30 of target & Top-30 of DS
        ds_top = set(s for s, _ in sorted(role_canon["Data Scientist"].items(),
                                          key=lambda kv: -kv[1])[:30])
        t_top = sorted(role_canon[tgt].items(), key=lambda kv: -kv[1])[:30]
        missing = [(s, n) for s, n in t_top if s not in ds_top and not s.startswith("__")]
        # Sort by composite difficulty
        missing.sort(key=lambda sn: -float(diff.get(sn[0], {}).get("composite_z", 0)))
        skills = [s for s, _ in missing][:15]

        if not skills:
            ax.set_title(f"{tgt}: no missing skills"); continue

        comps = ["gradient_z", "salary_z", "sd_z", "hhi_z", "idf_z"]
        comp_labels = ["Seniority gradient", "Salary premium", "Demand/supply", "Employer concentration", "Vocabulary jargon"]
        colors = ["#4c78a8", "#d62728", "#f58518", "#54a24b", "#9c755f"]

        # Stack with shifted z (only positive contributions for visualization)
        stacks = []
        for c in comps:
            vals = []
            for s in skills:
                v = float(diff.get(s, {}).get(c, 0))
                vals.append(max(v, 0))
            stacks.append(vals)

        bottom = np.zeros(len(skills))
        for vals, col, lab in zip(stacks, colors, comp_labels):
            ax.bar(skills, vals, bottom=bottom, color=col, label=lab)
            bottom += np.array(vals)

        ax.set_title(f"DS → {tgt}: hardest missing skills (sum of positive z-scores)",
                     fontweight="bold", fontsize=11)
        ax.set_ylabel("Σ(z+)")
        ax.tick_params(axis="x", rotation=35)
        for label in ax.get_xticklabels():
            label.set_horizontalalignment("right")
        if ax is axes[0]:
            ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    plt.tight_layout()
    out = HERE / "02_difficulty_breakdown.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


def main():
    chart_jaccard_vs_effort()
    chart_distance_rank_swap()
    chart_skill_landscape()
    chart_difficulty_breakdown()


if __name__ == "__main__":
    main()
