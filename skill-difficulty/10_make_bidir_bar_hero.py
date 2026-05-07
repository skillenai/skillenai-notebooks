"""Hero image v2: bidirectional small-multiples bar chart.

Each panel = one skill, with 4 horizontal bars (one per signal) centered on
a vertical zero line. Bars extending right = above-universe-average (positive
z-score). Bars extending left = below-universe-average. Missing salary
(skill not in regression sample) shows as a gray dashed placeholder.

Improvement over the radar:
- Negative salary coefficients (prompt engineering -21%, data labeling -39%)
  are visible — bars actually point left.
- Each bar label shows the raw signal value, not a normalized number.
- The "shape of hard" — many bars going right — is still readable across
  panels but no longer hides negatives.
"""
import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent

HARDEST = [
    ("diffusion models",        "Research peak"),
    ("representation learning", "Research peak"),
    ("reward modeling",         "Post-training"),
    ("JAX",                     "Engineering peak ★"),
    ("distributed training",    "Engineering peak"),
]

EASIEST = [
    ("data labeling",       "Bottom of universe"),
    ("react",               "Frontend"),
    ("prompt engineering",  "AIE plumbing"),
    ("llm apis",            "AIE plumbing"),
    ("javascript",          "Frontend"),
]

# Signals in display order (top-to-bottom in each panel)
SIGNALS = [
    ("Seniority gradient",   "gradient_z",         "gradient",        "{:.2f}"),
    ("Salary premium",       "salary_coef_z",      "salary_coef",     "salary_pct"),
    ("Academic depth",       "scholarly_ratio_z",  "scholarly_ratio", "{:.2f}"),
    ("Prereq depth",         "depth_z",            "depth",           "{}"),
]


def load_data():
    by_skill = {}
    with open(HERE / "difficulty_index.csv") as f:
        for r in csv.DictReader(f):
            by_skill[r["canonical_skill"].lower()] = r

    # Determine global z-range so x-axis is consistent across panels
    all_z = []
    for r in by_skill.values():
        for _, z_col, _, _ in SIGNALS:
            try:
                all_z.append(float(r[z_col]))
            except (ValueError, KeyError):
                pass
    z_min, z_max = min(all_z), max(all_z)
    return by_skill, z_min, z_max


def format_value(skill_row, raw_col, fmt):
    raw = skill_row.get(raw_col)
    if raw in (None, ""):
        return "n/a"
    if fmt == "salary_pct":
        if raw in ("0", "0.0"):
            return "n/a"
        return f"{(math.exp(float(raw))-1)*100:+.1f}%"
    try:
        return fmt.format(float(raw))
    except (ValueError, TypeError):
        return str(raw)


def is_missing_salary(skill_row):
    return skill_row.get("salary_coef") in (None, "", "0", "0.0")


def draw_panel(ax, skill_row, x_lim, label_left=False):
    n_sig = len(SIGNALS)
    y_positions = np.arange(n_sig)[::-1]  # top signal at top

    # Vertical zero line
    ax.axvline(0, color="#888888", linewidth=0.8, zorder=1)

    for i, (label, z_col, raw_col, fmt) in enumerate(SIGNALS):
        y = y_positions[i]
        try:
            z = float(skill_row[z_col])
        except (ValueError, KeyError):
            z = 0.0
        is_salary = (z_col == "salary_coef_z")
        missing = is_salary and is_missing_salary(skill_row)

        if missing:
            ax.barh(y, 0.4, left=-0.2, height=0.55, color="#eeeeee",
                    hatch="///", edgecolor="#bbbbbb", linewidth=0.4, zorder=2)
            ax.text(0, y, "n/a", va="center", ha="center", fontsize=7.5,
                    color="#999999", style="italic", zorder=4)
        else:
            color = "#d62728" if z >= 0 else "#1f77b4"
            ax.barh(y, z, height=0.6, color=color, alpha=0.85, zorder=3,
                    edgecolor="white", linewidth=0.5)
            # Value label at the bar tip
            value_str = format_value(skill_row, raw_col, fmt)
            x_offset = 0.08 if z >= 0 else -0.08
            ha = "left" if z >= 0 else "right"
            ax.text(z + x_offset, y, value_str, va="center", ha=ha,
                    fontsize=8.5, color="#222", fontweight="bold", zorder=5)

    ax.set_yticks(y_positions)
    if label_left:
        ax.set_yticklabels([s[0] for s in SIGNALS], fontsize=8.5)
    else:
        ax.set_yticklabels([])
    ax.set_xlim(x_lim)
    ax.set_xticks([])  # x-axis labels in the figure title only
    for spine in ["top", "right", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)


def main():
    by_skill, z_min, z_max = load_data()

    # Symmetric x-limit with breathing room for value labels
    span = max(abs(z_min), abs(z_max))
    x_lim = (-span * 1.4, span * 1.4)

    fig = plt.figure(figsize=(20, 10.5))
    gs = fig.add_gridspec(2, 5, hspace=0.7, wspace=0.55,
                           left=0.085, right=0.99, top=0.78, bottom=0.05)

    def _panel(row_idx, i, skill, tag):
        ax = fig.add_subplot(gs[row_idx, i])
        row = by_skill.get(skill.lower())
        if not row:
            ax.set_title(f"{skill}\n(missing)", fontsize=10)
            return
        draw_panel(ax, row, x_lim, label_left=(i == 0))
        comp = float(row["composite_z"])
        # Two-line title: skill on line 1, tag + composite on line 2
        ax.set_title(f"{skill}\n{tag}  ·  z = {comp:+.2f}",
                     fontsize=10.5, fontweight="bold", pad=6, linespacing=1.3)

    for i, (skill, tag) in enumerate(HARDEST):
        _panel(0, i, skill, tag)
    for i, (skill, tag) in enumerate(EASIEST):
        _panel(1, i, skill, tag)

    fig.text(0.5, 0.96, "What hard looks like  vs.  what easy looks like",
             ha="center", fontsize=18, fontweight="bold")
    fig.text(0.5, 0.928,
             "Bars are z-scored against the universe of 222 AI/ML/DS skills  ·  "
             "right = above mean  ·  left = below mean  ·  label is the raw signal",
             ha="center", fontsize=10.5, color="#555555")
    fig.text(0.5, 0.905,
             "red = harder than average  ·  blue = easier than average or salary penalty  ·  "
             "hatched gray = skill not in salary regression sample",
             ha="center", fontsize=9.5, color="#888888", style="italic")

    # Vertical row labels on the far left
    fig.text(0.012, 0.62, "5 HARDEST",
             ha="left", va="center", fontsize=14, fontweight="bold",
             color="#d62728", rotation=90)
    fig.text(0.012, 0.21, "5 EASIEST",
             ha="left", va="center", fontsize=14, fontweight="bold",
             color="#1f77b4", rotation=90)

    out = HERE / "00_hero_bidir.png"
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
