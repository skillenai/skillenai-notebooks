#!/usr/bin/env python3
"""Iterating on the hero image. Tone: mystery ("how is this possible?"), not a flex.
Skillenai palette (cyan->violet) for us; Jellyfish baseline muted to gray."""
import json, sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import LinearSegmentedColormap

OUT = sys.argv[1] if len(sys.argv) > 1 else "hero_iter.png"

D = json.load(open("weekly_data.json"))
W = D["weeks"]
xs = np.array([w["tokens"] for w in W], float)
prs = np.array([w["prs"] for w in W], float)
a, b = D["jellyfish_curve"]["a"], D["jellyfish_curve"]["b"]
curve = lambda x: a*np.log(x) + b
CEIL = D["jellyfish_curve"]["pr_ceiling"]

# --- Skillenai palette ---
SK_CYAN, SK_VIOLET = "#12c2d6", "#7b3ff2"
BRAND = LinearSegmentedColormap.from_list("brand", [SK_CYAN, SK_VIOLET])
BASE = "#c2c2cc"        # the crowd / Jellyfish baseline
BASE_LINE = "#a7a7b4"
INK = "#1a1a2e"
GRID = "#ececf2"
tokfmt = FuncFormatter(lambda v,_: f"{v/1e6:.0f}M" if v < 1e9 else f"{v/1e9:.1f}B")

fig, ax = plt.subplots(figsize=(12, 7.5))
fig.patch.set_facecolor("white")

# --- the crowd: muted baseline curve + obedient dots ---
xc = np.logspace(np.log10(3.5e7), np.log10(5e8), 300)
ax.plot(xc, curve(xc), color=BASE_LINE, lw=2.6, zorder=3, solid_capstyle="round")
xt = np.logspace(np.log10(3.8e7), np.log10(4.4e8), 40)
yt = curve(xt) + 0.10*np.sin(np.arange(40)*2.3) + 0.06*np.cos(np.arange(40)*5.1)
ax.scatter(xt, yt, s=26, color=BASE, alpha=0.8, zorder=4, edgecolor="none")
ax.scatter([3.4e8],[4.15], s=26, color=BASE, alpha=0.8, zorder=4)

# agentic barrier
ax.axvline(5e7, ls=(0,(6,4)), color="#8a8a98", lw=1.2, zorder=2)
ax.text(5.3e7, 39, "AGENTIC BARRIER", rotation=90, va="top", ha="left",
        fontsize=8, color="#8a8a98", fontweight="bold")
# ceiling
ax.axhline(CEIL, ls=":", color="#8a8a98", lw=1.2, zorder=2)
ax.text(3.6e7, CEIL+0.5, "the plateau  ~4 PRs/week", fontsize=8.5, color="#8a8a98")

# --- the anomaly: our 8 weekly points, ONE colour (one person) + cyan halo ---
for x, y in zip(xs, prs):
    ax.scatter([x],[y], s=760, color=SK_CYAN, alpha=0.13, zorder=5, edgecolor="none")  # outer halo
    ax.scatter([x],[y], s=430, color=SK_CYAN, alpha=0.18, zorder=5, edgecolor="none")  # inner halo
ax.scatter(xs, prs, s=195, color=SK_VIOLET, zorder=6, edgecolor="white", lw=1.9)

med_x, med_y = float(np.median(xs)), float(np.median(prs))

# --- mystery copy ---
fig.suptitle("Two Headwinds of AI Development", x=0.5, y=0.965,
             fontsize=17, fontweight="bold", color=INK)
ax.text(0.5, 1.05,
        "Grey is a million developers. Every purple dot is one person — after hours.",
        transform=ax.transAxes, ha="center", fontsize=12, color=SK_VIOLET, style="italic")

# pointer to the crowd — short, nearly straight down to the curve
ax.annotate("1,000,000 developers",
            xy=(2.75e8, 3.25), xytext=(2.75e8, 10.5),
            fontsize=10.5, color="#7a7a88", ha="center",
            arrowprops=dict(arrowstyle="-|>", color="#b3b3bf", lw=1.5,
                            connectionstyle="arc3,rad=0.0"))
# pointer to the anomaly — short, to the top dot
ax.annotate("one person · eight weeks",
            xy=(7.55e8, 36), xytext=(3.6e8, 38.7),
            fontsize=10.5, color=INK, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=SK_VIOLET, lw=1.7,
                            connectionstyle="arc3,rad=-0.12"))
# the mystery, in the open void mid-left
ax.text(1.15e8, 21.5, "how?", fontsize=36, fontweight="bold", color=SK_VIOLET,
        ha="center", va="center")

ax.set_xscale("log")
ax.set_xlim(3.5e7, 1.5e9)
ax.set_ylim(0, 40)
ax.set_xlabel("Tokens per developer per week", fontsize=11)
ax.set_ylabel("Merged PRs per developer per week", fontsize=11)
ax.xaxis.set_major_formatter(tokfmt)
ax.grid(True, which="both", color=GRID, lw=0.6)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.text(0.0, -0.13, "Baseline chart & curve: Jellyfish Research (1M developer-weeks). "
        "Coloured points: one solo developer, Jun–Jul 2026.",
        transform=ax.transAxes, fontsize=8, color="#9a9aa6")
fig.tight_layout(rect=(0,0,1,0.93))
fig.savefig(OUT, dpi=140, facecolor="white")
print("wrote", OUT)
