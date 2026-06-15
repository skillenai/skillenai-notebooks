#!/usr/bin/env python3
"""Charts for the three-surfaces / runtime-vs-frameworks analysis."""
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams.update({
    "figure.dpi": 150, "font.size": 12, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "font.family": "DejaVu Sans",
})
ORCH = "#d1495b"     # fading
RUNT = "#1f7a5a"     # rising
MCP_C = "#6b5b95"    # steady integration layer
BRAND = "#e08a00"


def load(path):
    rows = list(csv.DictReader(open(path)))
    return rows


def month_labels(rows):
    return [r["month"] for r in rows]


news = load("camps_news.csv")
blog = load("camps_blog.csv")

# ---- Chart 1: the crossover (brand-independent composition share) ----
m = month_labels(news)
strict_share = [int(r["Interaction (strict)"]) /
                (int(r["Interaction (strict)"]) + int(r["Orchestration frameworks"])) * 100
                for r in news]
x = np.arange(len(m))
fig, ax = plt.subplots(figsize=(11, 6))
ax.axhspan(50, 100, color=RUNT, alpha=0.05)
ax.axhspan(0, 50, color=ORCH, alpha=0.05)
ax.axhline(50, color="#888", lw=1, ls="--")
ax.plot(x, strict_share, "-o", color=RUNT, lw=3, ms=8)
for xi, yi in zip(x, strict_share):
    ax.annotate(f"{yi:.0f}%", (xi, yi), textcoords="offset points",
                xytext=(0, 11), ha="center", fontsize=10, color="#222")
ax.set_xticks(x)
ax.set_xticklabels([mm[2:] for mm in m], rotation=0)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.set_ylabel("Low-level runtime share of\n(runtime + orchestration) mentions")
ax.set_title("How to build an agent: the conversation flipped in 2026\n"
             "Skillenai news corpus · brand-independent (excludes 'Claude Code', 'computer use')",
             fontsize=13, loc="left")
ax.text(0.01, 0.93, "above the line = low-level tools (bash, file-edit, code-exec, agent SDK) win the mention",
        transform=ax.transAxes, fontsize=9, color=RUNT)
ax.text(0.01, 0.05, "below the line = orchestration frameworks (LangChain/LangGraph, RAG plumbing) win",
        transform=ax.transAxes, fontsize=9, color=ORCH)
fig.tight_layout()
fig.savefig("01_news_crossover.png", bbox_inches="tight")
plt.close(fig)

# ---- Chart 2: per-10k mention rates, three camps over time (news) ----
def per10k(rows, key):
    return [int(r[key]) / int(r["total"]) * 1e4 for r in rows]


fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(x, per10k(news, "Orchestration frameworks"), "-o", color=ORCH, lw=2.5,
        label="Orchestration frameworks (LangChain/LangGraph, RAG/vector-DB)")
ax.plot(x, per10k(news, "Interaction (strict)"), "-o", color=RUNT, lw=2.5,
        label="Low-level runtime (code-exec, sandbox, bash/file-edit, Agent SDK)")
ax.plot(x, per10k(news, "MCP"), "-o", color=MCP_C, lw=2.5,
        label="MCP (integration layer)")
ax.set_xticks(x)
ax.set_xticklabels([mm[2:] for mm in m])
ax.set_ylabel("Mentions per 10,000 news articles")
ax.set_title("Frameworks fade, runtime rises, MCP holds steady\n"
             "Skillenai news corpus, monthly mention rate", fontsize=13, loc="left")
ax.legend(fontsize=10, loc="upper left", framealpha=0.9)
ax.text(0.99, -0.13, "pre-2026 months are thin (hundreds of articles/mo) and noisier; the 2026 trend is the robust signal",
        transform=ax.transAxes, fontsize=8, color="#888", ha="right")
fig.tight_layout()
fig.savefig("02_news_per10k.png", bbox_inches="tight")
plt.close(fig)

# ---- Chart 3: cross-surface snapshot (leading/lagging cascade) ----
# cumulative per-10k from phrase_prevalence snapshot
surf = ["Jobs\n(what employers require)", "Blog\n(tutorials / how-tos)", "News\n(frontier discourse)"]
orch = [310.4, 296.7, 205.9]
runt = [25.8, 167.7, 274.2]
mcp = [73.6, 263.7, 217.1]
xs = np.arange(len(surf))
w = 0.26
fig, ax = plt.subplots(figsize=(11, 6))
ax.bar(xs - w, orch, w, color=ORCH, label="Orchestration frameworks")
ax.bar(xs, runt, w, color=RUNT, label="Low-level runtime (strict)")
ax.bar(xs + w, mcp, w, color=MCP_C, label="MCP (integration layer)")
for i in range(len(surf)):
    for off, val in [(-w, orch[i]), (0, runt[i]), (w, mcp[i])]:
        ax.annotate(f"{val:.0f}", (xs[i] + off, val), textcoords="offset points",
                    xytext=(0, 4), ha="center", fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(surf)
ax.set_ylabel("Mentions per 10,000 documents")
ax.set_title("The leading/lagging cascade: news has flipped, hiring hasn't\n"
             "Cumulative mention rate by surface", fontsize=13, loc="left")
ax.set_ylim(0, 370)
ax.legend(fontsize=10, framealpha=0.95, loc="upper center", ncol=3)
ax.annotate("12:1", (xs[0], 322), ha="center", fontsize=11, color=ORCH, weight="bold")
fig.tight_layout()
fig.savefig("03_cross_surface.png", bbox_inches="tight")
plt.close(fig)

print("wrote 01_news_crossover.png, 02_news_per10k.png, 03_cross_surface.png")
