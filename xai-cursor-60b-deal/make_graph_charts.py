#!/usr/bin/env python3
"""Graph-native charts for the xAI-Cursor analysis."""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DIR = Path(__file__).parent

# ================================================================
# Chart 6: Cursor co-required with each coding product (jobs)
# From graph query: MATCH (Cursor)<-[:MENTIONS]-(j:job)-[:MENTIONS]->(product)
# ================================================================
pairs = [
    ("Claude Code", 561),
    ("Claude", 326),
    ("GitHub Copilot", 270),
    ("ChatGPT", 129),
    ("Gemini", 105),
    ("Windsurf", 92),
    ("Grok", 8),
]
fig, ax = plt.subplots(figsize=(10, 5.5))
names = [p[0] for p in pairs]
vals = [p[1] for p in pairs]
colors = ["#d62728" if n == "Grok" else "#2ca02c" if n in ("Claude Code", "Claude") else "#1f77b4" for n in names]
bars = ax.barh(names, vals, color=colors)
ax.invert_yaxis()
for bar, v in zip(bars, vals):
    ax.text(v + 8, bar.get_y() + bar.get_height()/2, f"{v}", va="center", fontsize=10)
ax.set_xlabel("Jobs requiring Cursor AND this product")
ax.set_title("Jobs that co-require Cursor + another AI coding tool\nGrok appears in 8 — Claude Code in 561")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(DIR / "06_cursor_coreq_jobs.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 7: Bridge document density between product/company pairs
# From graph query: count(distinct d) where d MENTIONS both
# ================================================================
bridges = [
    ("Claude Code ↔ Anthropic", 3308, "first-party"),
    ("Cursor ↔ Anthropic",      730,  "third-party"),
    ("Cursor ↔ OpenAI",         726,  "third-party"),
    ("Grok ↔ xAI",              424,  "first-party"),
    ("Grok ↔ Anthropic",        321,  "third-party"),
    ("Claude Code ↔ xAI",       116,  "third-party"),
    ("Cursor ↔ xAI (pre-deal)", 55,   "third-party"),
]
fig, ax = plt.subplots(figsize=(10, 5.5))
labels = [b[0] for b in bridges]
vals = [b[1] for b in bridges]
colors = []
for l, v, t in bridges:
    if "Cursor ↔ xAI" in l:
        colors.append("#d62728")
    elif t == "first-party":
        colors.append("#2ca02c")
    else:
        colors.append("#1f77b4")
bars = ax.barh(labels, vals, color=colors)
ax.invert_yaxis()
for bar, v in zip(bars, vals):
    ax.text(v + 40, bar.get_y() + bar.get_height()/2, f"{v:,}", va="center", fontsize=10)
ax.set_xlabel("Distinct documents mentioning both entities")
ax.set_title("Bridge-document density across product↔company pairs\n(Graph query: MATCH (a)<-[:MENTIONS]-(d)-[:MENTIONS]->(b))")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(DIR / "07_bridge_density.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 8: Internal hiring-stack comparison (xAI vs Anthropic vs Cursor)
# ================================================================
xai_stack = [
    ("Grok", 52), ("Kubernetes", 14), ("Terraform", 10),
    ("ArgoCD", 6), ("Grafana", 5), ("Ansible", 5), ("Pulumi", 5),
    ("AI systems", 4), ("Prometheus", 3),
]
anth_stack = [
    ("Claude", 446), ("Claude Code", 128), ("Claude API", 63),
    ("Claude.ai", 50), ("Claude Enterprise", 28), ("MCP", 22),
    ("Claude Developer Platform", 21), ("Claude for Work", 21),
    ("Claude for Enterprise", 18), ("BigQuery", 20),
]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for ax, stack, title, color in [
    (ax1, anth_stack, "Anthropic — 9 distinct Claude product SKUs in hiring", "#2ca02c"),
    (ax2, xai_stack, "xAI — Grok + infrastructure (no product-eng breadth)", "#d62728"),
]:
    labels = [s[0] for s in stack[::-1]]
    vals = [s[1] for s in stack[::-1]]
    ax.barh(labels, vals, color=color)
    ax.set_xlabel("Job postings requiring this product")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)

fig.suptitle("What does each company hire for, in its own job postings?", fontsize=12)
fig.tight_layout()
fig.savefig(DIR / "08_internal_hiring_stacks.png", dpi=150)
plt.close(fig)

print("Saved 3 additional graph-derived charts.")
