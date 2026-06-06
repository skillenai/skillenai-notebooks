#!/usr/bin/env python3
"""Generate figures for synthetic-breakout-may-2026 analysis."""
import json
import os
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import requests

API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]
API_URL = "https://api.skillenai.com"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
HERE = Path(__file__).parent

plt.rcParams.update({"font.size": 11, "axes.titlesize": 13, "axes.labelsize": 11})


def post(body, retries=4):
    for i in range(retries):
        r = requests.post(f"{API_URL}/v1/query/search", json=body, headers=HEADERS, timeout=60)
        if r.status_code == 429:
            time.sleep(2 ** (i + 1))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limit")


# Verified data from earlier exploration
TOP_PERSONAE = [
    ("Daniel Mercer", 381, 208, 3.72),
    ("Jordan Ellis", 114, 102, 2.83),
    ("Jordan Mercer", 64, 53, 1.65),
    ("Alex Morgan", 45, 30, 1.50),
    ("Alex Mercer", 41, 31, 1.25),
    ("Marcus Ellison", 37, 35, 1.05),
    ("Avery Collins", 32, 31, 2.07),
    ("Jordan Hale", 27, 27, 2.36),
    ("Marcus Ellery", 22, 21, 1.45),
    ("Maya Chen", 22, 21, 1.21),
    ("Ethan Mercer", 20, None, None),
    ("Jordan Vale", 17, None, None),
    ("Maya Thornton", 15, None, None),
    ("Avery Morgan", 14, None, None),
    ("Maya Thompson", 13, None, None),
    ("Avery Cole", 12, None, None),
    ("Marcus Hale", 12, None, None),
    ("Avery Mitchell", 10, None, None),
    ("Jordan Blake", 10, None, None),
]

REAL_BREAKOUTS = [
    # (name, domain, role, apr_count, may_count, apr_auth, may_auth)
    ("Rod Trent", "rodtrent.substack.com", "Microsoft Sentinel / security influencer (Substack)", 31, 51, 0.53, 0.96),
    ("Ruben Hassid", "ruben.substack.com", "AI commentator (Substack)", 25, 10, 2.03, 3.37),
    ("Alex Merced", "datalakehousehub.com", "Dremio dev advocate · Apache Iceberg specialist", 265, 209, 0.99, 1.54),
    ("Marin Ivezic", "postquantum.com", "Post-quantum cryptography expert", 11, 65, 0.25, 0.37),
    ("Frank Landymore", "futurism.com", "Futurism.com staff writer (AI desk)", 25, 30, 3.71, 4.43),
    ("Joe Wilkins", "futurism.com", "Futurism.com staff writer", 27, 25, 2.72, 3.55),
    ("The Deep View", "archive.thedeepview.com", "AI newsletter (high-velocity)", 37, 25, 0.41, 1.59),
    ("Grant Harvey", "theneuron.ai", "The Neuron newsletter", 50, 40, 1.37, 1.92),
]


# ---------- Figure 1: April vs May byline distribution on network domains ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
months = ["April 2026", "May 2026"]

# Data from analysis
apr_total = 8583
apr_with_author = 38
apr_no_author = 8545
may_total = 1856
may_with_author = 1856  # all have author
may_distinct_authors = 221
may_no_author = 0

# Left panel: stacked bar comparing posts by byline status
ax = axes[0]
labels = ["April 2026", "May 2026"]
no_byline = [apr_no_author, may_no_author]
with_byline = [apr_with_author, may_with_author]
x = np.arange(len(labels))
width = 0.55
b1 = ax.bar(x, no_byline, width, label="No author byline", color="#cccccc", edgecolor="#666666")
b2 = ax.bar(x, with_byline, width, bottom=no_byline, label="With author byline", color="#d62728", edgecolor="#7a1414")
for i, (n, w) in enumerate(zip(no_byline, with_byline)):
    if n > 0:
        ax.text(i, n / 2, f"{n:,}\n({n/(n+w)*100:.1f}%)", ha="center", va="center", color="#333", fontweight="bold")
    if w > 0:
        ax.text(i, n + w / 2, f"{w:,}\n({w/(n+w)*100:.1f}%)", ha="center", va="center", color="white", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("Blog posts ingested")
ax.set_title("Same 333 domains, two strategies")
ax.legend(loc="upper right", framealpha=0.95)
ax.spines[["top", "right"]].set_visible(False)

# Right panel: distinct authors per month
ax = axes[1]
distinct = [1, 221]  # April effectively 1 (most no-byline + a handful of stragglers)
# Use a clearer measure: April distinct *named* authors = 30 (top-30 saturated)
distinct_named = [30, 221]
bars = ax.bar(labels, distinct_named, width, color=["#cccccc", "#d62728"], edgecolor="#666666")
for bar, v in zip(bars, distinct_named):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 4, f"{v}", ha="center", fontweight="bold", fontsize=14)
ax.set_ylabel("Distinct author bylines")
ax.set_title("Synthetic persona inventory")
ax.set_ylim(0, 250)
ax.spines[["top", "right"]].set_visible(False)

fig.suptitle("April → May 2026: A content farm adds bylines", fontsize=15, fontweight="bold", y=1.02)
fig.text(0.5, -0.02,
         "Same 333 cheap cloud-themed domains in both months. In April, 99.6% of posts had no author. In May, the operator attached 221 distinct fake-persona bylines to the same kind of LLM-generated content.",
         ha="center", fontsize=9.5, style="italic", color="#444", wrap=True)
plt.tight_layout()
fig.savefig(HERE / "01_byline_strategy_shift.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Figure 2: Persona network — domains per persona + cross-persona overlap ----------
fig, ax = plt.subplots(figsize=(11, 6.5))
names = [p[0] for p in TOP_PERSONAE[:10]]
posts = [p[1] for p in TOP_PERSONAE[:10]]
doms = [p[2] for p in TOP_PERSONAE[:10]]
auth = [p[3] for p in TOP_PERSONAE[:10]]

y = np.arange(len(names))
ax.barh(y, posts, color="#d62728", alpha=0.85, label="May posts", edgecolor="#7a1414")
ax.barh(y, doms, color="#1f77b4", alpha=0.7, label="Distinct domains used", edgecolor="#0e4173")
for i, (p, d, a) in enumerate(zip(posts, doms, auth)):
    ratio = p / d
    label = f"  {p} posts / {d} domains = {ratio:.1f} per domain · auth={a:.2f}"
    ax.text(p + 5, i, label, va="center", fontsize=9)
ax.set_yticks(y); ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel("Count")
ax.set_title("Top 10 'authors' in the persona network — May 2026", fontweight="bold")
ax.legend(loc="lower right")
ax.set_xlim(0, max(posts) * 1.55)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.5, -0.04,
         "Every persona spreads posts across many domains. Daniel Mercer alone used 208 distinct domains in May; on average, each persona's posts are spread ~1.0–1.8 per domain.",
         ha="center", fontsize=9.5, style="italic", color="#444")
plt.tight_layout()
fig.savefig(HERE / "02_persona_volume_vs_domains.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Figure 3: Shared-domain matrix ----------
SHARED_DOMAINS = [
    ("deployed.cloud", ["Avery Collins", "Alex Mercer", "Alex Morgan", "Jordan Hale", "Maya Chen", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("midways.cloud",  ["Alex Mercer", "Jordan Hale", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis", "Marcus Ellison"]),
    ("toggle.top",     ["Alex Mercer", "Marcus Ellery", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis", "Marcus Ellison"]),
    ("typescript.website", ["Marcus Ellery", "Maya Chen", "Daniel Mercer", "Jordan Ellis", "Marcus Ellison"]),
    ("opensoftware.cloud", ["Alex Mercer", "Alex Morgan", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("typescript.page",    ["Avery Collins", "Alex Mercer", "Alex Morgan", "Daniel Mercer"]),
    ("devtools.cloud",     ["Maya Chen", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("evaluate.live",      ["Alex Mercer", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("promptly.cloud",     ["Avery Collins", "Maya Chen", "Daniel Mercer", "Jordan Ellis"]),
    ("oorbyte.com",        ["Maya Chen", "Jordan Mercer", "Daniel Mercer", "Marcus Ellison"]),
    ("thecloudlife.net",   ["Avery Collins", "Maya Chen", "Daniel Mercer", "Marcus Ellison"]),
    ("preprod.cloud",      ["Alex Mercer", "Jordan Hale", "Jordan Mercer", "Daniel Mercer"]),
    ("datastore.cloud",    ["Avery Collins", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("net-work.pro",       ["Alex Morgan", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
    ("quickfix.cloud",     ["Avery Collins", "Alex Mercer", "Maya Chen", "Daniel Mercer"]),
    ("untied.dev",         ["Marcus Ellery", "Jordan Mercer", "Daniel Mercer", "Jordan Ellis"]),
]
personae_in_grid = ["Daniel Mercer", "Jordan Ellis", "Jordan Mercer", "Alex Mercer", "Alex Morgan", "Marcus Ellison", "Avery Collins", "Jordan Hale", "Maya Chen", "Marcus Ellery"]
M = np.zeros((len(SHARED_DOMAINS), len(personae_in_grid)))
for i, (_, who) in enumerate(SHARED_DOMAINS):
    for j, p in enumerate(personae_in_grid):
        if p in who:
            M[i, j] = 1

fig, ax = plt.subplots(figsize=(11, 7))
ax.imshow(M, cmap="Reds", aspect="auto", vmin=0, vmax=1.3)
ax.set_xticks(range(len(personae_in_grid))); ax.set_xticklabels(personae_in_grid, rotation=35, ha="right")
ax.set_yticks(range(len(SHARED_DOMAINS))); ax.set_yticklabels([d for d, _ in SHARED_DOMAINS])
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i, j] > 0:
            ax.text(j, i, "✕", ha="center", va="center", color="white", fontweight="bold", fontsize=12)
ax.set_title("Shared domains × shared personae — May 2026", fontweight="bold")
fig.text(0.5, -0.03,
         "Each ✕ = the persona published on the domain in May 2026. Eight different 'authors' all publish to deployed.cloud. The infrastructure is shared, the bylines are interchangeable.",
         ha="center", fontsize=9.5, style="italic", color="#444")
plt.tight_layout()
fig.savefig(HERE / "03_shared_domain_matrix.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Figure 4: Authority percentile context ----------
percentiles = [50, 75, 90, 95, 99, 99.5, 99.9]
values = [0.40, 0.73, 1.51, 2.74, 4.82, 5.10, 5.15]
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(percentiles, values, marker="o", linewidth=2.5, color="#1f77b4", markersize=8, label="May 2026 blog index authorAuthority")
ax.axhline(y=0.71, color="#666", linestyle=":", label=f"Mean = 0.71")
# Mark the personae
markers = [("Daniel Mercer", 3.72, 95.5), ("Jordan Ellis", 2.83, 90.5), ("Avery Collins", 2.07, 89), ("Jordan Hale", 2.36, 90)]
for name, v, est_pct in markers:
    ax.scatter([est_pct], [v], color="#d62728", s=120, zorder=5)
    ax.annotate(f"{name}\n(avg auth {v})", xy=(est_pct, v), xytext=(est_pct - 12, v + 0.4),
                fontsize=9, color="#7a1414",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2))
ax.set_xlabel("Percentile of authorAuthority across May 2026 blog posts (N=99,344 posts; ~31.6K with authority)")
ax.set_ylabel("authorAuthority (per-post)")
ax.set_title("Synthetic personae land in the top 5% on authority", fontweight="bold")
ax.legend(loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(alpha=0.3)
fig.text(0.5, -0.03,
         "The system's authorAuthority signal rewards topical relevance + volume. LLM-generated AI/MLOps content satisfies both trivially. The 50th percentile real-author score is 0.40; the synthetic personae sit at 2–4.",
         ha="center", fontsize=9.5, style="italic", color="#444", wrap=True)
plt.tight_layout()
fig.savefig(HERE / "04_authority_percentile.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Figure 5: Daniel Mercer daily timeline ----------
days = list(range(12, 32))  # 12..31
counts = [1, 15, 9, 6, 0, 1, 0, 11, 29, 53, 94, 59, 29, 4, 15, 10, 14, 15, 8, 8]
assert len(days) == len(counts)
fig, ax = plt.subplots(figsize=(11, 4.5))
bars = ax.bar(days, counts, color="#d62728", edgecolor="#7a1414")
ax.set_xlabel("Day of May 2026")
ax.set_ylabel("Posts ingested")
ax.set_title("Daniel Mercer's birth and burst — May 2026", fontweight="bold")
ax.set_xticks(days)
ax.spines[["top", "right"]].set_visible(False)
ax.annotate(f"Peak: 94 posts/day", xy=(22, 94), xytext=(25, 80), fontsize=10, color="#7a1414",
            arrowprops=dict(arrowstyle="->", color="#d62728"))
ax.annotate("Persona activated\nMay 12", xy=(12, 1), xytext=(13, 50), fontsize=10, color="#444",
            arrowprops=dict(arrowstyle="->", color="#666"))
fig.text(0.5, -0.04,
         "381 posts published in 20 days across 208 distinct domains. Persona had no prior history — 0 posts in April.",
         ha="center", fontsize=9.5, style="italic", color="#444")
plt.tight_layout()
fig.savefig(HERE / "05_daniel_mercer_timeline.png", dpi=150, bbox_inches="tight")
plt.close()


# ---------- Figure 6: Real human breakouts ----------
fig, ax = plt.subplots(figsize=(12, 6.5))
names = [r[0] for r in REAL_BREAKOUTS]
apr_c = np.array([r[3] for r in REAL_BREAKOUTS])
may_c = np.array([r[4] for r in REAL_BREAKOUTS])
apr_a = np.array([r[5] for r in REAL_BREAKOUTS])
may_a = np.array([r[6] for r in REAL_BREAKOUTS])

x = np.arange(len(names))
width = 0.35

# Two panels: volume change, authority change
ax2 = ax.twinx()
b1 = ax.bar(x - width/2, apr_c, width, label="April posts", color="#a6cee3", edgecolor="#1f5d8c")
b2 = ax.bar(x + width/2, may_c, width, label="May posts", color="#1f77b4", edgecolor="#0e4173")
# Authority dots on right axis
ax2.scatter(x - width/2, apr_a, color="#fb9a99", s=120, edgecolors="#7a1414", linewidth=1.5, zorder=5, label="April authority")
ax2.scatter(x + width/2, may_a, color="#d62728", s=120, edgecolors="#7a1414", linewidth=1.5, zorder=5, label="May authority")
for xi, (a, m) in enumerate(zip(apr_a, may_a)):
    ax2.plot([xi - width/2, xi + width/2], [a, m], color="#7a1414", lw=1.5, alpha=0.5)

ax.set_xticks(x); ax.set_xticklabels(names, rotation=25, ha="right")
ax.set_ylabel("Posts per month")
ax2.set_ylabel("Avg authorAuthority")
ax.set_title("Real human breakouts — the signal beneath the noise", fontweight="bold")
ax.legend(loc="upper left")
ax2.legend(loc="upper right")
ax.spines[["top"]].set_visible(False)
ax2.spines[["top"]].set_visible(False)
fig.text(0.5, -0.05,
         "Bars = post volume (left axis). Dots = avg authorAuthority (right axis, line connects April → May). Rod Trent and Marin Ivezic gain on both axes; Ruben Hassid trades volume for authority; Alex Merced posts less but his authority rises with the Iceberg/Dremio content surge.",
         ha="center", fontsize=9.5, style="italic", color="#444")
plt.tight_layout()
fig.savefig(HERE / "06_real_breakouts.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"Wrote 6 figures to {HERE}")
