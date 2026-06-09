"""Figures for the authoritative-data-viz listicle.

Inputs come from queries already run during the skn-insights session; this
script just renders the small JSON snapshots into PNGs.
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent

picks = json.loads((HERE / "raw_picks.json").read_text())
authors = json.loads((HERE / "authors.json").read_text())

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "DejaVu Sans",
})

SKN_BLUE = "#1f6feb"
SKN_PURPLE = "#7c3aed"
SKN_TEAL = "#0891b2"
SKN_AMBER = "#f59e0b"


def fig_authors():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    rows = sorted(authors, key=lambda r: r["avg_authorAuthority"], reverse=True)
    names = [f"{r['author']}\n{r['domain']}" for r in rows]
    aa = [r["avg_authorAuthority"] for r in rows]
    n = [r["total_posts_on_domain"] for r in rows]
    colors = [SKN_BLUE, SKN_PURPLE, SKN_TEAL, SKN_AMBER, "#6b7280"]
    bars = ax.barh(names, aa, color=colors)
    ax.invert_yaxis()
    ax.set_xlabel("avg authorAuthority (PageRank-style citation score)")
    ax.set_title("Top 5 most authoritative data-viz authors in the Skillenai blog corpus")
    for bar, count, score in zip(bars, n, aa):
        ax.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height() / 2,
                f"AA={score:.2f}   n={count}", va="center", fontsize=10)
    ax.set_xlim(0, max(aa) * 1.35)
    fig.tight_layout()
    fig.savefig(HERE / "01_top_authors.png", bbox_inches="tight")
    plt.close(fig)


def fig_articles():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    arts = picks["articles"]
    labels = []
    da_vals = []
    aa_vals = []
    for a in arts:
        t = a["title"]
        if len(t) > 60:
            t = t[:57] + "..."
        labels.append(f"{t}\n{a['author']} @ {a['domain']}")
        da_vals.append((a["domainAuthority"] or 0) * 1e6)
        aa_vals.append(a["authorAuthority"] or 0)
    y = np.arange(len(labels))
    width = 0.4
    ax.barh(y - width / 2, da_vals, width, color=SKN_BLUE, label="DA × 1e6")
    ax.barh(y + width / 2, aa_vals, width, color=SKN_PURPLE, label="authorAuthority")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("authority score (DA scaled ×1e6 to share axis with AA)")
    ax.set_title("Top 5 most authoritative articles ABOUT data visualization")
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "02_top_articles.png", bbox_inches="tight")
    plt.close(fig)


def fig_viz_pieces():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    viz = picks["viz"]
    labels = []
    da_vals = []
    aa_vals = []
    for v in viz:
        t = v["title"]
        if len(t) > 60:
            t = t[:57] + "..."
        author = v.get("author") or "(no byline)"
        labels.append(f"{t}\n{author} @ {v['domain']}")
        da_vals.append((v["domainAuthority"] or 0) * 1e6)
        aa_vals.append(v["authorAuthority"] or 0)
    y = np.arange(len(labels))
    width = 0.4
    ax.barh(y - width / 2, da_vals, width, color=SKN_TEAL, label="DA × 1e6")
    ax.barh(y + width / 2, aa_vals, width, color=SKN_AMBER, label="authorAuthority")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("authority score (DA scaled ×1e6 to share axis with AA)")
    ax.set_title("Top 5 most interesting data visualizations in the corpus")
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "03_top_viz_pieces.png", bbox_inches="tight")
    plt.close(fig)


def fig_corpus_overview():
    """How thin is the dataviz slice of the corpus?"""
    fig, ax = plt.subplots(figsize=(7, 5))
    total = 428774
    dataviz = 3883
    other = total - dataviz
    sizes = [dataviz, other]
    labels = [f"data-viz blog posts\n({dataviz:,}, 0.9%)", f"other blog posts\n({other:,})"]
    colors = [SKN_PURPLE, "#e5e7eb"]
    ax.pie(sizes, labels=labels, colors=colors, startangle=90,
            wedgeprops={"linewidth": 1.5, "edgecolor": "white"},
            textprops={"fontsize": 10})
    ax.set_title("Data-viz slice of prod-enriched-blog\n(428,774 posts total)")
    fig.tight_layout()
    fig.savefig(HERE / "04_corpus_overview.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_authors()
    fig_articles()
    fig_viz_pieces()
    fig_corpus_overview()
    print("wrote 4 figures to", HERE)
