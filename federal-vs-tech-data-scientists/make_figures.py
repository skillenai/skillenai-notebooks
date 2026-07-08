#!/usr/bin/env python3
"""
Figures for "Two Data-Science Worlds" — the supply side of federal vs private
data scientists (Skillenai x Live Data / workforce.ai).

All values are captured from the Live Data (workforce.ai) People analytics run
described in README.md. No re-query is performed here; the script just renders.

Palette: Skillenai logo gradient, cyan -> violet.
"""
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

CYAN = "#06b6d4"     # private / frontier tech
VIOLET = "#7c3aed"   # federal
INK = "#1e293b"
GRID = "#e2e8f0"
MUTE = "#94a3b8"

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.edgecolor": GRID,
    "axes.linewidth": 1.0,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
})

SRC = "Source: Skillenai analysis of Live Data (workforce.ai) People profiles, July 2026"


def brand(fig, y=0.005):
    fig.text(0.008, y, "Skillenai", fontsize=11, fontweight="bold", color=VIOLET)
    fig.text(0.075, y, "× Live Data", fontsize=10, color=MUTE)


# ---------------------------------------------------------------------------
# Fig 1 — Education funnels: what federal vs private data scientists studied
# ---------------------------------------------------------------------------
# % of the cohort holding a degree in each field (multi-degree; cols don't sum 100)
# fed N=252, priv N=7,683.  '*' = below the field's top-25 threshold (<~1%).
fields = [
    "Statistics", "Computer Science", "Economics", "Data Science",
    "Mathematics", "Biostatistics", "Epidemiology", "Psychology",
    "Physics", "Business Analytics", "Mechanical Eng.*", "Industrial Eng.*",
]
fed = [4.4, 6.7, 4.4, 4.8, 4.0, 3.2, 5.2, 3.6, 2.4, 2.0, 0.0, 0.0]
priv = [9.4, 7.2, 5.3, 4.7, 4.1, 1.5, 0.3, 0.8, 2.3, 3.8, 2.1, 1.8]

order = np.argsort([f - p for f, p in zip(fed, priv)])  # federal-tilted at top
fields = [fields[i] for i in order]
fed = [fed[i] for i in order]
priv = [priv[i] for i in order]

y = np.arange(len(fields))
h = 0.4
fig, ax = plt.subplots(figsize=(10.5, 7.2))
ax.barh(y + h/2, fed, height=h, color=VIOLET, label="Federal DS (N=252)")
ax.barh(y - h/2, priv, height=h, color=CYAN, label="Private-tech DS (N=7,683)")
for yi, (f, p) in enumerate(zip(fed, priv)):
    ax.text(f + 0.12, yi + h/2, f"{f:.1f}%", va="center", fontsize=8.5, color=VIOLET)
    ax.text(p + 0.12, yi - h/2, f"{p:.1f}%", va="center", fontsize=8.5, color=CYAN)
ax.set_yticks(y)
ax.set_yticklabels(fields)
ax.set_xlabel("Share of the cohort holding a degree in this field")
ax.set_xlim(0, 10.6)
ax.set_title("Different people, not just different job posts\n"
             "Federal data scientists come up through domain & social science; "
             "private ones through statistics & engineering",
             fontsize=13, fontweight="bold", loc="left")
ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.55), frameon=False)
ax.grid(axis="x", color=GRID)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.text(0.008, 0.038, "* Mechanical/Industrial Eng. fall below the federal cohort's top-25 fields (<~1%); a private-DS feeder with no federal analog.",
         fontsize=7.5, color=MUTE)
fig.text(0.99, 0.010, SRC, fontsize=7.5, color=MUTE, ha="right")
brand(fig, y=0.010)
fig.tight_layout(rect=[0, 0.055, 1, 1])
fig.savefig("01_education_funnels.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Fig 2 — Title role-history proxy (of 100 federal DS, ever held a title with...)
# ---------------------------------------------------------------------------
roles = ["Researcher / Fellow", "Analyst", "Academic (prof/postdoc/PhD)",
         "Statistician", "Engineer (any)", "Health / clinical domain",
         "ML / AI", "Software / Developer"]
vals = [64, 48, 31, 25, 25, 18, 13, 11]
# identity vs builder colouring
builder = {"ML / AI", "Software / Developer", "Engineer (any)"}
colors = [CYAN if r in builder else VIOLET for r in roles]

order = np.argsort(vals)
roles = [roles[i] for i in order]
vals = [vals[i] for i in order]
colors = [colors[i] for i in order]

fig, ax = plt.subplots(figsize=(10, 5.6))
ax.barh(roles, vals, color=colors)
for yi, v in enumerate(vals):
    ax.text(v + 0.7, yi, f"{v}%", va="center", fontsize=9.5, color=INK)
ax.set_xlabel("Share of 100 federal data scientists who have EVER held a title containing this")
ax.set_xlim(0, 72)
ax.set_title("Federal data scientists are researchers and analysts by career — rarely builders",
             fontsize=13, fontweight="bold", loc="left")
ax.grid(axis="x", color=GRID)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=VIOLET, label="Research / analyst identity"),
                   Patch(color=CYAN, label="Hands-on builder (ML / software / eng)")],
          loc="lower right", frameon=False)
fig.text(0.99, 0.02, SRC + " (n=100 profiles)", fontsize=7.5, color=MUTE, ha="right")
brand(fig)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig("02_title_history.png", bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------------------
# Fig 3 — Two closed doors: where federal DS come from and go (COVER)
# ---------------------------------------------------------------------------
in_labels = ["Academia / research", "Non-frontier private\nindustry",
             "Government", "Nonprofit / NGO", "Contractor", "Big Tech /\nfrontier AI"]
in_vals = [46, 32, 8, 8, 5, 1]
out_labels = ["Another federal\nagency", "Cleared contractor /\nconsulting",
              "Private / other", "Big Tech /\nfrontier AI"]
out_vals = [76, 18, 6, 0.3]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 6.2))

def flow_panel(ax, labels, vals, base_color, title, sub):
    y = np.arange(len(labels))[::-1]
    colors = []
    for lab in labels:
        colors.append("#e11d48" if lab.startswith("Big Tech") else base_color)
    ax.barh(y, vals, color=colors)
    for yi, v in zip(y, vals):
        txt = f"{v:.1f}%" if v < 1 else f"{v:.0f}%"
        ax.text(v + 1.2, yi, txt, va="center", fontsize=10, fontweight="bold",
                color="#e11d48" if v <= 1 else INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.set_xlim(0, 88)
    ax.set_title(title, fontsize=12.5, fontweight="bold", loc="left", pad=10)
    ax.set_xlabel(sub, fontsize=9, color=MUTE)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

flow_panel(axL, in_labels, in_vals, VIOLET,
           "Where federal data scientists come FROM",
           "mid-career entrants, n=76 of 100 profiles")
flow_panel(axR, out_labels, out_vals, CYAN,
           "Where they GO next",
           "identifiable next destinations, cohort N=1,181")

fig.suptitle("Two weakly-connected worlds: the frontier-tech door is shut in both directions",
             fontsize=15, fontweight="bold", x=0.01, ha="left", y=0.99)
fig.text(0.01, 0.925, "Academia and older-economy industry feed federal data science. "
         "Big Tech sends ~1 in 76 in — and takes 4 of 1,181 out.",
         fontsize=10.5, color=INK)
fig.text(0.99, 0.015, SRC, fontsize=7.5, color=MUTE, ha="right")
brand(fig, y=0.015)
fig.tight_layout(rect=[0, 0.03, 1, 0.9])
fig.savefig("03_flows_in_out.png", bbox_inches="tight")
plt.close(fig)

print("wrote 01_education_funnels.png, 02_title_history.png, 03_flows_in_out.png")
