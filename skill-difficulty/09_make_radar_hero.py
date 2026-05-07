"""Hero image: small-multiples radar (web) chart showing the 4 difficulty
signals as a profile shape per skill.

Layout: 2 rows × 5 columns. Top row = 5 hardest skills (data-driven, but
selected to span profile variety AND include the headline skill JAX). Bottom
row = 5 easiest skills (strict bottom by composite).

Each radar has 4 axes:
  Seniority gradient  (top)
  Salary premium     (right)
  Academic depth     (bottom)
  Prereq depth       (left)

Axis scale: min-max over the full 222-skill universe → [0, 1]. Means a value
of 1 on any axis is the *hardest skill in the universe* on that signal.
Missing salary (n<50 in USD-salary sample) is shown as half-transparent fill
on the salary axis at the median position, with a note.
"""
import csv
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent

# Editorial pick — includes the headline skill JAX even though it's #13 by
# composite (most other top-10 entries are profile-similar research peaks;
# JAX is the unique engineering+salary avatar)
HARDEST = [
    ("diffusion models", "Research peak"),
    ("representation learning", "Research peak"),
    ("reward modeling", "Post-training"),
    ("JAX", "Engineering peak (headline)"),
    ("distributed training", "Engineering peak"),
]

# Strict bottom-5 by composite z (after dropping the data-labeling extreme
# outlier that dominates the visual scale)
EASIEST = [
    ("data labeling", "Bottom of universe"),
    ("react", "Frontend"),
    ("prompt engineering", "AIE plumbing"),
    ("llm apis", "AIE plumbing"),
    ("javascript", "Frontend"),
]

AXES = [
    ("Seniority gradient",  "gradient_z"),
    ("Salary premium",      "salary_coef_z"),
    ("Academic depth",      "scholarly_ratio_z"),
    ("Prereq depth",        "depth_z"),
]


def load_difficulty():
    by_skill = {}
    raw_vals = {a[1]: [] for a in AXES}
    with open(HERE / "difficulty_index.csv") as f:
        for r in csv.DictReader(f):
            by_skill[r["canonical_skill"].lower()] = r
            for _, col in AXES:
                try:
                    raw_vals[col].append(float(r[col]))
                except (ValueError, KeyError):
                    pass
    # Min-max ranges
    ranges = {col: (min(raw_vals[col]), max(raw_vals[col])) for col in raw_vals}
    return by_skill, ranges


def normalize(skill_row, ranges):
    """Return list of [0,1] values per axis in AXES order, plus a 'missing_salary' flag."""
    out = []
    missing_salary = False
    for label, col in AXES:
        v = float(skill_row[col])
        # Detect "missing salary" (skill not in regression sample → got z=0 in compose step)
        if col == "salary_coef_z" and (skill_row.get("salary_coef") in (None, "", "0", "0.0")):
            missing_salary = True
        lo, hi = ranges[col]
        norm = (v - lo) / (hi - lo) if hi > lo else 0.5
        out.append(max(0.0, min(1.0, norm)))
    return out, missing_salary


def draw_radar(ax, values, color, alpha_fill=0.35, label_axes=False, missing_salary=False):
    n = len(values)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    vals = values + values[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Background grid rings at 0.25, 0.5, 0.75
    for r in [0.25, 0.5, 0.75, 1.0]:
        ax.plot(np.linspace(0, 2*np.pi, 100), [r]*100, color="#cccccc",
                linewidth=0.5, alpha=0.6)

    # Spokes
    for a in angles[:-1]:
        ax.plot([a, a], [0, 1], color="#cccccc", linewidth=0.5, alpha=0.6)

    # The skill profile
    ax.plot(angles, vals, color=color, linewidth=2.0)
    ax.fill(angles, vals, color=color, alpha=alpha_fill)

    # Vertex markers
    ax.scatter(angles[:-1], vals[:-1], color=color, s=30, zorder=5,
               edgecolors="white", linewidths=1)

    # Mark missing salary axis with an X if applicable
    if missing_salary:
        salary_idx = next(i for i, a in enumerate(AXES) if a[1] == "salary_coef_z")
        ax.scatter([angles[salary_idx]], [values[salary_idx]],
                   color="#888888", marker="x", s=60, zorder=6, linewidths=2)

    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])

    if label_axes:
        ax.set_xticklabels([a[0] for a in AXES], fontsize=8)
    else:
        ax.set_xticklabels(["", "", "", ""])
    ax.spines["polar"].set_visible(False)


def main():
    by_skill, ranges = load_difficulty()

    fig = plt.figure(figsize=(17, 10))
    gs = fig.add_gridspec(2, 5, hspace=1.0, wspace=0.45,
                           left=0.03, right=0.99, top=0.81, bottom=0.04)

    HARD_COLOR = "#d62728"
    EASY_COLOR = "#4c78a8"

    def _stat_subtitle(row):
        sal = row["salary_coef"]
        if sal in (None, "", "0", "0.0"):
            sal_str = "n/a"
        else:
            sal_str = f"{(math.exp(float(sal)) - 1)*100:+.1f}%"
        return (f"gradient {float(row['gradient']):.2f}  ·  "
                f"salary {sal_str}\n"
                f"scholarly {float(row['scholarly_ratio']):.2f}  ·  "
                f"prereq depth {row['depth']}")

    def _draw_panel(ax_position, skill, tag, color, is_first):
        ax = fig.add_subplot(ax_position, projection="polar")
        row = by_skill.get(skill.lower())
        if not row:
            ax.set_title(f"{skill}\n(missing)", fontsize=10)
            return
        vals, missing_sal = normalize(row, ranges)
        draw_radar(ax, vals, color, label_axes=is_first, missing_salary=missing_sal)
        ax.set_title(f"{skill}\n{tag}", fontsize=11, fontweight="bold", pad=8,
                     linespacing=1.3)
        ax.text(0.5, -0.32, _stat_subtitle(row), transform=ax.transAxes,
                ha="center", fontsize=8.5, color="#444444", linespacing=1.4)

    for i, (skill, tag) in enumerate(HARDEST):
        _draw_panel(gs[0, i], skill, tag, HARD_COLOR, i == 0)

    for i, (skill, tag) in enumerate(EASIEST):
        _draw_panel(gs[1, i], skill, tag, EASY_COLOR, i == 0)

    fig.text(0.5, 0.965, "What hard looks like  vs.  what easy looks like",
             ha="center", fontsize=16, fontweight="bold")
    fig.text(0.5, 0.935,
             "Profile shape across 4 difficulty signals, normalized to the universe of 222 measured AI/ML/DS skills",
             ha="center", fontsize=10, color="#555555")
    fig.text(0.5, 0.912,
             "Outer ring = hardest in the universe on that signal  ·  × = no salary coef (n<50 USD-salaried postings)",
             ha="center", fontsize=9, color="#888888", style="italic")

    fig.text(0.5, 0.872, "▼  5 hardest skills  ·  engineering + research peaks  ▼",
             ha="center", fontsize=12, fontweight="bold", color=HARD_COLOR)
    fig.text(0.5, 0.418, "▼  5 easiest skills  ·  the bottom of the difficulty distribution  ▼",
             ha="center", fontsize=12, fontweight="bold", color=EASY_COLOR)

    out = HERE / "00_hero_radar.png"
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
