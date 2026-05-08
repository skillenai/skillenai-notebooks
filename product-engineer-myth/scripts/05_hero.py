"""Hero image for the product-engineer-myth post.

Matches the visual style of skillenai-notebooks/ds-vs-mle-vs-aie/role-skills-comparison.png:
- Title at top
- Grouped horizontal bar chart with 3 colored bars per skill
- Banded sections with tinted backgrounds + boxed role labels on the right
- Skills grouped by which role(s) they belong to
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "00_hero.png"

# Colors matching reference (DS=blue, MLE=purple, AIE=orange)
# Map: PM=blue, SWE=purple, PE=orange
COLOR_PM = "#4D8DE0"
COLOR_SWE = "#9B7BD7"
COLOR_PE = "#F5A623"

# Light tinted backgrounds for each section
BG_FOUNDATION = "#F5F5F5"
BG_PM = "#EEF4FB"   # very light blue
BG_SWE = "#F4F0FA"  # very light purple
BG_PE = "#FDF5E8"   # very light orange

# Sections — list of (skill_label, PM_pct, SWE_pct, PE_pct)
SECTIONS = [
    (
        "Engineering Foundation",
        BG_FOUNDATION,
        None,  # no role color tag for shared section
        [
            ("Python",                2.15, 33.18, 38.44),
            ("AWS",                   1.11, 21.98, 17.87),
            ("Kubernetes",            0.82, 17.85,  9.61),
            ("Distributed systems",   1.65, 17.16, 14.11),
            ("CI/CD",                 0.00, 15.46,  8.26),
            ("Docker",                0.00, 13.37,  5.26),
            ("Go",                    0.00, 12.40,  9.16),
            ("Testing",               1.65,  9.88, 10.36),
            ("Observability",         2.42,  9.84, 10.81),
        ],
    ),
    (
        "Product Engineer Stack",
        BG_PE,
        ("Product Engineer", COLOR_PE),
        [
            ("TypeScript",            0.00, 21.80, 57.51),
            ("React",                 0.00, 21.83, 55.11),
            ("Postgres",              0.00, 14.12, 28.23),
            ("Next.js",               0.00,  2.69, 18.77),
            ("Node.js",               0.00, 10.32, 16.37),
            ("LLM",                   4.13,  3.33, 14.26),
            ("Full-stack development",0.00,  2.29,  9.31),
            ("API design",            2.78,  4.55,  9.01),
            ("Redis",                 0.00,  4.51,  7.66),
            ("Cursor",                1.03,  1.66,  6.46),
            ("Frontend development",  0.00,  1.37,  6.76),
            ("FastAPI",               0.00,  2.45,  6.01),
        ],
    ),
    (
        "Software Engineer (Enterprise)",
        BG_SWE,
        ("Software Engineer", COLOR_SWE),
        [
            ("Java",                  0.00, 20.84,  4.35),
            ("C++",                   0.00, 11.98,  0.00),
            ("Microservices",         0.00,  7.88,  2.70),
            ("Azure",                 0.80,  7.91,  4.50),
            ("REST APIs",             0.00,  7.01,  3.75),
            ("Kafka",                 0.00,  6.42,  3.15),
            ("C#",                    0.00,  6.09,  2.10),
            ("Linux",                 0.00,  5.79,  0.00),
        ],
    ),
    (
        "Product Manager Core",
        BG_PM,
        ("Product Manager", COLOR_PM),
        [
            ("Product management",   38.62,  0.00,  0.00),
            ("Product roadmap",      22.21,  0.00,  0.00),
            ("Data analysis",        18.88,  1.61,  3.45),
            ("Product strategy",     15.99,  0.00,  0.00),
            ("Experimentation",      10.88,  0.97,  2.10),
            ("A/B testing",           9.61,  0.95,  2.85),
            ("Stakeholder management",8.87,  0.00,  0.00),
            ("User research",         7.77,  0.00,  0.00),
            ("Cross-functional collab.",7.45,0.00,  0.00),
            ("Data-driven decisions", 6.53,  0.00,  0.00),
        ],
    ),
]


def main() -> None:
    GAP = 0.6  # visual gap (in y-units) between sections

    # First pass: compute y position for each skill row, and index spans per section
    y_positions = []
    skill_labels = []
    pm_vals = []; swe_vals = []; pe_vals = []
    section_spans = []  # (title, bg, tag, idx_start, idx_end)
    cursor = 0.0
    skill_idx = 0
    for title, bg, tag, items in SECTIONS:
        idx_start = skill_idx
        for label, pm, swe, pe in items:
            y_positions.append(cursor)
            skill_labels.append(label)
            pm_vals.append(pm); swe_vals.append(swe); pe_vals.append(pe)
            cursor += 1
            skill_idx += 1
        section_spans.append((title, bg, tag, idx_start, skill_idx - 1))
        cursor += GAP

    fig_h = max(13, 0.42 * cursor)
    fig, ax = plt.subplots(figsize=(18, fig_h))

    y_positions = np.array(y_positions)
    h = 0.26
    ax.barh(y_positions - h, pm_vals,  h, color=COLOR_PM,  label="Product Manager",   zorder=3, edgecolor="white", linewidth=0.4)
    ax.barh(y_positions,     swe_vals, h, color=COLOR_SWE, label="Software Engineer", zorder=3, edgecolor="white", linewidth=0.4)
    ax.barh(y_positions + h, pe_vals,  h, color=COLOR_PE,  label="Product Engineer",  zorder=3, edgecolor="white", linewidth=0.4)

    # Draw the shaded section backgrounds (full-width, behind bars)
    x_lo, x_hi = -2, 82
    for title, bg, tag, start, end in section_spans:
        # find y-extents from the y_positions array
        y_start = y_positions[start] - h - 0.45
        y_end = y_positions[end] + h + 0.45
        ax.axhspan(y_start, y_end, facecolor=bg, edgecolor="none", zorder=1)
        # role tag boxed label on the right
        if tag is not None:
            tag_text, tag_color = tag
            ax.text(
                x_hi - 1.5, (y_start + y_end) / 2, tag_text,
                ha="right", va="center", fontsize=12, fontweight="bold",
                color=tag_color,
                bbox=dict(facecolor="white", edgecolor=tag_color, linewidth=1.5,
                          boxstyle="round,pad=0.4"),
                zorder=4,
            )
        else:
            ax.text(
                x_hi - 1.5, (y_start + y_end) / 2, title,
                ha="right", va="center", fontsize=11, fontweight="bold",
                color="#888",
                bbox=dict(facecolor="white", edgecolor="#bbb", linewidth=1.0,
                          boxstyle="round,pad=0.4"),
                zorder=4,
            )

    # Style
    ax.set_yticks(y_positions)
    ax.set_yticklabels(skill_labels, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(cursor - GAP - 0.3, -1.0)
    ax.set_xlabel("% of postings requiring skill", fontsize=12)
    ax.set_title(
        "How Three Roles Diverge: Skill Demand Across 35,067 Job Postings",
        fontsize=17, fontweight="bold", pad=18,
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#888")
    ax.tick_params(axis="x", labelsize=10)
    ax.grid(axis="x", linestyle=":", color="#ccc", alpha=0.7, zorder=0)
    ax.set_axisbelow(True)

    # Legend at bottom-right
    handles = [
        mpatches.Patch(color=COLOR_PM,  label="Product Manager"),
        mpatches.Patch(color=COLOR_SWE, label="Software Engineer"),
        mpatches.Patch(color=COLOR_PE,  label="Product Engineer"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=11,
              framealpha=0.95, edgecolor="#ccc")

    plt.tight_layout()
    plt.savefig(OUT, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
