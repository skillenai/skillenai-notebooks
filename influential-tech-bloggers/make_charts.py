#!/usr/bin/env python3
"""Build the three rankings, compute overlap, and emit the chart set."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).parent

authors = json.load(open(OUT / "authors_cleaned.json"))
domains = json.load(open(OUT / "domains_cleaned.json"))


def topn(items, key, n):
    return sorted(items, key=lambda x: -x[key])[:n]


# === Compute three top-30 author lists ============================
top_vol = topn(authors, "n_posts", 30)
top_auth = topn([a for a in authors if a["n_posts"] >= 8], "avg_authority", 30)
top_sum = topn(authors, "sum_authority", 30)


def overlap(a, b, k):
    A = {x["author"] for x in a[:k]}
    B = {x["author"] for x in b[:k]}
    return len(A & B), len(A | B), A & B


print("=== Overlap between top-20 lists ===")
for label, a, b in [
    ("vol vs auth", top_vol, top_auth),
    ("vol vs sum",  top_vol, top_sum),
    ("auth vs sum", top_auth, top_sum),
]:
    inter, union, names = overlap(a, b, 20)
    print(f"  {label}:  {inter}/{20}   Jaccard={inter/union:.3f}   shared={sorted(names)}")

# === Stash for README ============================
summary = {
    "top_volume_30": top_vol,
    "top_authority_30": top_auth,
    "top_sum_30": top_sum,
    "n_authors_total": len(authors),
}
(OUT / "rankings_summary.json").write_text(json.dumps(summary, indent=2))


# === Chart 1: three side-by-side bar charts of top 15 ============
def short_author(a, n=28):
    s = a.get("author", "")
    s = s.replace("🎭", "").strip()
    return (s[: n - 1] + "…") if len(s) > n else s


fig, axes = plt.subplots(1, 3, figsize=(20, 9))
fig.suptitle("Three views of 'most influential tech blogger' — and the lists barely overlap",
             fontsize=15, fontweight="bold", y=0.995)

panels = [
    ("By post volume\n(rewards content farms + podcasts)", top_vol[:15], "n_posts", "#post-fetched", "#a48cff"),
    ("By per-post authority\n(min 8 posts; rewards thought-leaders)", top_auth[:15], "avg_authority", "avg authority score", "#2cb6a0"),
    ("By volume × authority\n(rewards consistent operators)", top_sum[:15], "sum_authority", "Σ authority", "#e76b5a"),
]

for ax, (title, items, field, xlabel, color) in zip(axes, panels):
    items = list(reversed(items))  # top -> bottom
    labels = [short_author(a) for a in items]
    values = [a[field] for a in items]
    ax.barh(range(len(values)), values, color=color, edgecolor="#222", linewidth=0.4)
    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(labels, fontsize=10)
    for i, (a, v) in enumerate(zip(items, values)):
        if field == "avg_authority":
            extra = f"  n={a['n_posts']}"
        elif field == "n_posts":
            extra = f"  auth={a['avg_authority']:.1f}"
        else:
            extra = f"  n={a['n_posts']} ×{a['avg_authority']:.1f}"
        ax.text(v, i, extra, va="center", fontsize=8, color="#444")
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_title(title, fontsize=11, pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig(OUT / "01_three_rankings.png", dpi=150, bbox_inches="tight")
print(f"Wrote {OUT / '01_three_rankings.png'}")


# === Chart 2: Volume vs Authority scatter ===========================
fig, ax = plt.subplots(figsize=(12, 8))
xs = np.array([a["n_posts"] for a in authors])
ys = np.array([a["avg_authority"] for a in authors])

ax.scatter(xs, ys, s=14, alpha=0.35, color="#888", linewidth=0)

# Highlight named individuals (auth > 3.0 with at least 10 posts)
notable = [a for a in authors if (a["avg_authority"] >= 3.0 and a["n_posts"] >= 10) or a["sum_authority"] >= 200]
notable_set = {a["author"] for a in notable}
ax.scatter([a["n_posts"] for a in notable], [a["avg_authority"] for a in notable],
           s=42, color="#2cb6a0", edgecolor="#0a4f43", linewidth=0.7, zorder=3, label="High-influence (≥3 authority, ≥10 posts) or high-Σ")

# Label a curated subset to keep readable
manual_labels = {
    "John Gruber", "Simon Willison", "Lenny Rachitsky", "Gergely Orosz",
    "Nathan Lambert", "Ethan Mollick", "Ksenia Se", "José Valim",
    "Noah Smith", "Melanie Mitchell", "Drew Breunig", "Jack Clark",
    "Avi Chawla", "Greg Kamradt", "Alex Kantrowitz",
    "Peggy Smedley", "Tobias Macey", "Sam Charrington", "Jeffrey Palermo",
    "Andreas and Michael Wittig", "Wes Bos & Scott Tolinski - Full Stack JavaScript Web Developers",
    "Adam", "Jonathan Hall", "Alex Merced",
}
for a in authors:
    if a["author"] not in manual_labels:
        continue
    label = a["author"]
    if "Wes Bos" in label:
        label = "Wes Bos & S. Tolinski"
    if "Andreas" in label:
        label = "Wittig brothers"
    if a["author"] == "Adam":
        label = "Adam (Shostack)"
    ax.annotate(label, (a["n_posts"], a["avg_authority"]),
                xytext=(6, 4), textcoords="offset points", fontsize=9,
                color="#222", alpha=0.95)

ax.set_xscale("log")
ax.set_xlabel("Posts in Skillenai blog index (log scale)", fontsize=11)
ax.set_ylabel("Avg authorAuthority (per-post quality, system signal)", fontsize=11)
ax.set_title("Tech bloggers: post volume vs per-post authority\nThe top-right is empty. The high-authority writers cluster on the left; the high-volume cluster sits below auth = 2.",
             fontsize=12, pad=14)
ax.axhline(3.0, color="#aaa", linestyle="--", linewidth=0.8)
ax.text(2000, 3.05, "auth = 3.0", fontsize=8, color="#666")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig(OUT / "02_volume_vs_authority.png", dpi=150, bbox_inches="tight")
print(f"Wrote {OUT / '02_volume_vs_authority.png'}")


# === Chart 3: Top 25 domains by authority ==============================
top_dom_auth = sorted([d for d in domains if d["n_posts"] >= 8], key=lambda x: -x["avg_da"])[:25]
top_dom_vol = sorted(domains, key=lambda x: -x["n_posts"])[:25]

fig, axes = plt.subplots(1, 2, figsize=(18, 9))
fig.suptitle("Same split at the publication level — top 25 tech-blog domains",
             fontsize=14, fontweight="bold")

for ax, items, title, field, color in [
    (axes[0], list(reversed(top_dom_vol)), "By post volume", "n_posts", "#a48cff"),
    (axes[1], list(reversed(top_dom_auth)), "By avg domain authority (min 8 posts)", "avg_da", "#2cb6a0"),
]:
    labels = [d["domain"][:42] for d in items]
    if field == "avg_da":
        values = [d[field] * 1e6 for d in items]
        xlabel = "avg domainAuthority × 10⁶"
    else:
        values = [d[field] for d in items]
        xlabel = "post count"
    ax.barh(range(len(values)), values, color=color, edgecolor="#222", linewidth=0.4)
    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_title(title, fontsize=11, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig(OUT / "03_domains.png", dpi=150, bbox_inches="tight")
print(f"Wrote {OUT / '03_domains.png'}")


# === Chart 4: Substack share among top-25 by authority =================
def domain_class(d):
    if "substack.com" in d:
        return "Substack"
    if "futurism.com" in d:
        return "Tech tabloid (Futurism)"
    if d.endswith(".com") or d.endswith(".io") or d.endswith(".ai") or d.endswith(".co"):
        return "Independent / personal site"
    return "Other"


classes = [domain_class(a["domains"][0] if a["domains"] else "") for a in top_auth[:25]]
from collections import Counter

c = Counter(classes)
fig, ax = plt.subplots(figsize=(8, 5))
keys = sorted(c.keys(), key=lambda k: -c[k])
vals = [c[k] for k in keys]
ax.bar(keys, vals, color=["#7c5cff", "#e76b5a", "#2cb6a0", "#888"][: len(keys)])
for i, v in enumerate(vals):
    ax.text(i, v + 0.1, str(v), ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("# in top 25 by authority")
ax.set_title("Where do the high-authority tech bloggers actually publish?\nSubstack dominates: independent newsletters and personal sites, not branded media.",
             fontsize=11, pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig(OUT / "04_publication_homes.png", dpi=150, bbox_inches="tight")
print(f"Wrote {OUT / '04_publication_homes.png'}")
print("Done.")
