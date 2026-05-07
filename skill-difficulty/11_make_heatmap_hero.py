"""Hero image v3: divergent z-score heatmap.

Rows: 7 hardest + 7 easiest skills + 4 "interesting middle" cases (fine-tuning,
RAG, agentic workflows, causal inference) for context.
Columns: the 4 difficulty signals + composite z.
Cells: colored by z-score (red high / blue low / gray missing) with the raw
signal value printed inside. Honest about negatives and missing data.
"""
import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import numpy as np

HERE = Path(__file__).parent

HARDEST = [
    "generative modeling",
    "JAX",                # ★ headline — only skill with all 5 positive
    "reward modeling",
    "FSDP",
    "distributed training",
    "triton",
    "causal inference",
]

INTERESTING = [
    "agent architectures",
    "agentic workflows",
    "fine-tuning",
    "RAG",
]

EASIEST = [
    "javascript",
    "sql",
    "react",
    "prompt engineering",
    "data labeling",
]

SIGNALS = [
    ("Seniority\ngradient",  "gradient_z",  "gradient",     "{:.2f}"),
    ("Salary\npremium",      "salary_z",    "salary_coef",  "salary_pct"),
    ("Demand /\nsupply",     "sd_z",        "sd_log10",     "sd_ratio"),
    ("Employer\nconcentration","hhi_z",     "hhi",          "{:.3f}"),
    ("Vocabulary\njargon",   "idf_z",       "mean_idf",     "{:.2f}"),
    ("Composite\nz",         "composite_z", "composite_z",  "{:+.2f}"),
]


def load_data():
    by_skill = {}
    with open(HERE / "difficulty_index.csv") as f:
        for r in csv.DictReader(f):
            by_skill[r["canonical_skill"].lower()] = r
    return by_skill


def format_value(skill_row, raw_col, fmt):
    raw = skill_row.get(raw_col)
    if raw in (None, ""):
        return ""
    if fmt == "salary_pct":
        if raw in ("0", "0.0"):
            return "n/a"
        return f"{(math.exp(float(raw))-1)*100:+.1f}%"
    if fmt == "sd_ratio":
        # sd_log10 stored; display as ratio (10^x). High = blog-saturated, low = demand-heavy.
        try:
            return f"{10 ** float(raw):.2f}"
        except (ValueError, TypeError):
            return ""
    try:
        return fmt.format(float(raw))
    except (ValueError, TypeError):
        return str(raw)


def is_missing(skill_row, z_col, raw_col):
    """Cell is hatched-gray if the raw value is missing (and the z is therefore 0)."""
    raw = skill_row.get(raw_col)
    if raw in (None, ""):
        return True
    if z_col == "salary_z" and raw in ("0", "0.0"):
        return True
    return False


def main():
    by_skill = load_data()

    # Build rows in display order: hardest top → easiest bottom
    skills_in_order = HARDEST + INTERESTING + EASIEST
    section_breaks = [len(HARDEST), len(HARDEST) + len(INTERESTING)]

    n_rows = len(skills_in_order)
    n_cols = len(SIGNALS)

    z_matrix = np.full((n_rows, n_cols), np.nan)
    text_matrix = [[""] * n_cols for _ in range(n_rows)]
    missing_mask = np.zeros((n_rows, n_cols), dtype=bool)

    for i, skill in enumerate(skills_in_order):
        row = by_skill.get(skill.lower())
        if not row:
            continue
        for j, (_, z_col, raw_col, fmt) in enumerate(SIGNALS):
            try:
                z = float(row[z_col])
                z_matrix[i, j] = z
            except (ValueError, KeyError):
                pass
            text_matrix[i][j] = format_value(row, raw_col, fmt)
            if z_col != "composite_z" and is_missing(row, z_col, raw_col):
                missing_mask[i, j] = True
                text_matrix[i][j] = "n/a"
                z_matrix[i, j] = 0  # neutral cell color

    # Diverging colormap: blue (negative) → white (zero) → red (positive)
    cmap = LinearSegmentedColormap.from_list(
        "rwb", ["#3182bd", "#deebf7", "#ffffff", "#fee5d9", "#cb181d"]
    )
    vmax = max(abs(np.nanmin(z_matrix)), abs(np.nanmax(z_matrix)))
    vmax = min(vmax, 3.0)  # cap so the data labeling outlier doesn't squash everything
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    fig, ax = plt.subplots(figsize=(15, 11))

    # Plot heatmap
    img = ax.imshow(z_matrix, cmap=cmap, norm=norm, aspect="auto")

    # Overlay missing-data hatching
    for i, j in zip(*np.where(missing_mask)):
        ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                    fill=True, facecolor="#f0f0f0",
                                    hatch="//", edgecolor="#bbbbbb",
                                    linewidth=0.4))

    # Cell text
    for i in range(n_rows):
        for j in range(n_cols):
            txt = text_matrix[i][j]
            if not txt:
                continue
            z = z_matrix[i, j]
            color = "white" if (not missing_mask[i, j] and abs(z) > 1.4) else "#222"
            if missing_mask[i, j]:
                color = "#888"
            weight = "bold" if SIGNALS[j][1] == "composite_z" else "normal"
            ax.text(j, i, txt, ha="center", va="center", fontsize=10,
                    color=color, fontweight=weight)

    # Y-axis: skill names, with JAX in bold + star
    y_labels = []
    for s in skills_in_order:
        if s == "JAX":
            y_labels.append("★  JAX")
        else:
            y_labels.append(s)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(y_labels, fontsize=11)

    # Bold the JAX label
    for tick in ax.get_yticklabels():
        if "JAX" in tick.get_text():
            tick.set_fontweight("bold")
            tick.set_color("#cb181d")

    # X-axis: signal names at the top
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels([s[0] for s in SIGNALS], fontsize=11, fontweight="bold")
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.tick_params(axis="x", which="both", length=0)
    ax.tick_params(axis="y", which="both", length=0)

    # Section dividers (horizontal lines between groups)
    for sb in section_breaks:
        ax.axhline(sb - 0.5, color="#222222", linewidth=1.5)

    # Section labels on the right
    section_centers = [
        (len(HARDEST) - 1) / 2,
        len(HARDEST) + (len(INTERESTING) - 1) / 2,
        len(HARDEST) + len(INTERESTING) + (len(EASIEST) - 1) / 2,
    ]
    section_titles = [
        ("HARDEST", "#cb181d"),
        ("MIDDLE", "#666666"),
        ("EASIEST", "#3182bd"),
    ]
    for center, (title, color) in zip(section_centers, section_titles):
        ax.text(n_cols + 0.18, center, title, va="center", ha="left",
                fontsize=12, fontweight="bold", color=color, rotation=270)

    # Colorbar
    cbar = fig.colorbar(img, ax=ax, fraction=0.025, pad=0.07,
                         orientation="vertical", shrink=0.65)
    cbar.set_label("z-score relative to universe of 222 skills",
                   fontsize=9.5, color="#333")
    cbar.ax.tick_params(labelsize=8)

    # Grid lines between cells
    ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_visible(False)

    fig.suptitle("How 16 AI/ML/DS skills score on 5 difficulty signals",
                 fontsize=15, fontweight="bold", y=0.96)
    fig.text(0.5, 0.93,
             "Color = z-score against the universe of 222 measured skills  ·  "
             "cell label = raw signal value  ·  hatched gray = no data",
             ha="center", fontsize=10, color="#555")
    fig.text(0.5, 0.025,
             "★  JAX scores top-decile on every signal except vocabulary (where it ranks #2).  "
             "Demand/supply is blog-mentions per job-mention — low = demand-heavy.  "
             "Employer concentration is the Herfindahl index — high = specialist.  "
             "Prompt engineering carries a salary penalty AND the lowest jargon density.",
             ha="center", fontsize=9.5, color="#444", style="italic", wrap=True)

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])
    out = HERE / "00_hero_heatmap.png"
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {out.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
