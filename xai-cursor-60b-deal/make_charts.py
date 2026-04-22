#!/usr/bin/env python3
"""Charts for the xAI-Cursor $60B deal analysis."""
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

DIR = Path(__file__).parent

# Clean editorial + jobs mentions per AI coding product (from mentions_summary.json)
# Source types included: jobs, blog, news (editorial / labor demand signals)
products = [
    ("ChatGPT",        756,  7384, 3244),
    ("Claude",         1192, 5371, 2362),
    ("Claude Code",    1047, 5315, 1541),
    ("Gemini",         502,  2891, 1269),
    ("Cursor",         1231, 1773, 479),
    ("GitHub Copilot", 681,  1579, 345),
    ("Copilot",        339,  1162, 469),
    ("Grok",           73,   578,  296),
    ("Windsurf",       140,  365,  97),
]

# ================================================================
# Chart 1: stacked bar of mentions by source_type per product
# ================================================================
fig, ax = plt.subplots(figsize=(12, 6))
names = [p[0] for p in products]
jobs  = np.array([p[1] for p in products])
blogs = np.array([p[2] for p in products])
news  = np.array([p[3] for p in products])

x = np.arange(len(names))
ax.bar(x, jobs,  label="Jobs (labor demand)",   color="#1f77b4")
ax.bar(x, blogs, bottom=jobs, label="Blogs",    color="#ff7f0e")
ax.bar(x, news,  bottom=jobs+blogs, label="News", color="#2ca02c")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=30, ha="right")
ax.set_ylabel("Mentions (last ~6 weeks)")
ax.set_title("AI Coding Product Mentions by Source\nSkillenai index, 2026-03-01 → 2026-04-22")
ax.legend()
for i, (n, j, b, ne) in enumerate(products):
    total = j + b + ne
    ax.text(i, total + 200, f"{total:,}", ha="center", fontsize=9)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(DIR / "01_mentions_by_source.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 2: Jobs-only ranking — labor demand for each tool
# ================================================================
sorted_p = sorted(products, key=lambda p: p[1], reverse=True)
fig, ax = plt.subplots(figsize=(10, 5.5))
names_s = [p[0] for p in sorted_p]
jobs_s  = [p[1] for p in sorted_p]
colors = ["#d62728" if n == "Grok" else ("#1f77b4" if n == "Cursor" else "#999999") for n in names_s]
bars = ax.barh(names_s, jobs_s, color=colors)
for bar, v in zip(bars, jobs_s):
    ax.text(v + 20, bar.get_y() + bar.get_height()/2, f"{v:,}", va="center", fontsize=10)
ax.set_xlabel("Job postings mentioning the product")
ax.set_title("Labor-demand signal per AI coding product\nCursor leads; Grok is 16.9× behind")
ax.invert_yaxis()
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(DIR / "02_jobs_ranking.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 3: "Buzz vs adoption" — editorial mentions vs job mentions
# ================================================================
fig, ax = plt.subplots(figsize=(10, 7))
for name, j, b, ne in products:
    editorial = b + ne
    color = "#d62728" if name == "Grok" else ("#1f77b4" if name == "Cursor" else "#2ca02c" if name == "Claude Code" else "#999999")
    size = max(60, j * 0.5)
    ax.scatter(j, editorial, s=size, color=color, alpha=0.75, edgecolors="black")
    ax.annotate(name, (j, editorial), xytext=(8, 6), textcoords="offset points", fontsize=10)
# Reference line: adoption/buzz ratio of Cursor
cursor_ratio = 1773 + 479
cursor_jobs = 1231
xs = np.linspace(10, 1300, 50)
ax.plot(xs, xs * (cursor_ratio / cursor_jobs), "--", color="gray", alpha=0.6, label="Cursor-equivalent buzz:adoption ratio")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Labor-demand mentions (job postings, log)")
ax.set_ylabel("Editorial mentions (blog + news, log)")
ax.set_title("Buzz vs. adoption\nGrok: lots of talk, very little hiring. Cursor: inverse.")
ax.legend(loc="lower right")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(DIR / "03_buzz_vs_adoption.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 4: News/blog co-mention strength with Cursor
# ================================================================
# From news_comentions.json, Cursor_product row
cursor_comentions = [
    ("Claude Code", 1102),
    ("GitHub", 769),
    ("Anthropic", 672),
    ("OpenAI", 633),
    ("Claude", 536),
    ("GitHub Copilot", 478),
    ("Google", 460),
    ("ChatGPT", 392),
    ("Codex", 343),
    ("Windsurf", 338),
    ("Microsoft", 262),
    ("VS Code", 252),
    ("Gemini", 247),
    ("MCP", 148),
    ("Copilot", 140),
]
fig, ax = plt.subplots(figsize=(10, 6))
labels = [c[0] for c in cursor_comentions]
vals = [c[1] for c in cursor_comentions]
colors2 = ["#d62728" if l in ("Claude Code", "Anthropic", "Claude") else "#1f77b4" for l in labels]
bars = ax.barh(labels, vals, color=colors2)
ax.invert_yaxis()
ax.set_xlabel("News + blog articles co-mentioning Cursor and this entity")
ax.set_title("What gets mentioned alongside Cursor in the press\n(Anthropic/Claude/Claude Code in red — these are the \"Cursor is paired with\" complements)")
for bar, v in zip(bars, vals):
    ax.text(v + 15, bar.get_y() + bar.get_height()/2, f"{v:,}", va="center", fontsize=9)
ax.grid(axis="x", alpha=0.3)
# Add legend
red_patch = mpatches.Patch(color="#d62728", label="Anthropic-stack complement (entangled with Cursor workflows)")
blue_patch = mpatches.Patch(color="#1f77b4", label="Other")
ax.legend(handles=[red_patch, blue_patch], loc="lower right")
fig.tight_layout()
fig.savefig(DIR / "04_cursor_comentions.png", dpi=150)
plt.close(fig)

# ================================================================
# Chart 5: What appears in the same job posting as Cursor vs Grok
# ================================================================
cursor_skills = [
    ("Python", 506), ("Claude Code", 432), ("TypeScript", 373), ("AWS", 362),
    ("CI/CD", 362), ("React", 308), ("SQL", 277), ("Kubernetes", 260),
    ("Observability", 247), ("GitHub Copilot", 245), ("Claude", 210),
    ("Docker", 209), ("Node.js", 185), ("PostgreSQL", 170),
]
grok_skills = [
    ("Accent variation", 31), ("Prosody analysis", 31), ("Voice recording", 31),
    ("Sociolinguistics", 31), ("Cognitive science", 31), ("Phonology", 31),
    ("Speech recognition", 31), ("Training voice models", 31),
    ("Audio quality eval", 31), ("Intonation", 31), ("Annotation workflows", 31),
    ("Linguistics", 31), ("Audio data annotation", 31), ("Phonetics", 31),
]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.barh([s[0] for s in cursor_skills[::-1]], [s[1] for s in cursor_skills[::-1]], color="#1f77b4")
ax1.set_xlabel("Jobs co-mentioning skill + Cursor")
ax1.set_title("What jobs require Cursor?\nSoftware engineering stack (+ the other AI coding tools)")
ax1.grid(axis="x", alpha=0.3)

ax2.barh([s[0] for s in grok_skills[::-1]], [s[1] for s in grok_skills[::-1]], color="#d62728")
ax2.set_xlabel("Jobs co-mentioning skill + Grok")
ax2.set_title("What jobs require Grok?\nVoice/linguistic annotation (xAI internal data work)")
ax2.grid(axis="x", alpha=0.3)

fig.tight_layout()
fig.savefig(DIR / "05_skill_context_cursor_vs_grok.png", dpi=150)
plt.close(fig)

print("Saved 5 charts to", DIR)
