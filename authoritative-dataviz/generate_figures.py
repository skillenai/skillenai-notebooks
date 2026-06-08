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
    """How thin is the dataviz slice of the corpus, and where are the big outlets missing?"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: dataviz slice of corpus
    total = 428774
    dataviz = 3883
    other = total - dataviz
    sizes = [dataviz, other]
    labels = [f"data-viz blog posts\n({dataviz:,}, 0.9%)", f"other blog posts\n({other:,})"]
    colors = [SKN_PURPLE, "#e5e7eb"]
    wedges, texts = ax1.pie(sizes, labels=labels, colors=colors, startangle=90,
                             wedgeprops={"linewidth": 1.5, "edgecolor": "white"},
                             textprops={"fontsize": 10})
    ax1.set_title("Data-viz slice of prod-enriched-blog\n(428,774 posts total)")

    # Right: coverage gap of canonical dataviz outlets
    canonical = [
        ("nightingaledvs.com", 14),
        ("nytimes.com", 4),
        ("themarkup.org", 11),
        ("visualisingdata.com", 12),
        ("datajournalism.com", 19),
        ("flowingdata.com", 0),
        ("pudding.cool", 0),
        ("blog.datawrapper.de", 0),
        ("graphics.reuters.com", 0),
        ("policyviz.com", 0),
    ]
    canonical = sorted(canonical, key=lambda r: r[1], reverse=True)
    domains = [c[0] for c in canonical]
    counts = [c[1] for c in canonical]
    colors2 = [SKN_BLUE if c > 0 else "#ef4444" for c in counts]
    ax2.barh(domains, counts, color=colors2)
    ax2.invert_yaxis()
    ax2.set_xlabel("docs in prod-enriched-blog")
    ax2.set_title("Canonical dataviz outlets:\ncoverage gap in the Skillenai corpus")
    for i, c in enumerate(counts):
        ax2.text(c + 0.3, i, str(c), va="center", fontsize=10,
                  color="#7f1d1d" if c == 0 else "#374151")

    fig.tight_layout()
    fig.savefig(HERE / "04_corpus_overview.png", bbox_inches="tight")
    plt.close(fig)


def fig_pbn_reminder():
    """Small banner showing the PBN denylist removed N posts and N personae."""
    fig, ax = plt.subplots(figsize=(11, 2.4))
    ax.axis("off")
    txt = (
        "Methodology guardrails applied (every ranking respects these)\n\n"
        "■ 333-domain Private Blog Network denylist (SKI-376 synthetic-persona content farm)\n"
        "■ Junk-author filter: removes admin/Editor/Team/HTML/email/multi-comma multi-author strings\n"
        "■ Leaky source_type=blog domains removed (ATS listings, medical news, preprint servers)\n"
        "■ Authority signal: blogpost domainAuthority + authorAuthority (PageRank-style)"
    )
    ax.text(0.02, 0.5, txt, fontsize=11, va="center",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#fef3c7", edgecolor="#f59e0b", linewidth=1.4))
    fig.tight_layout()
    fig.savefig(HERE / "05_methodology_guardrails.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_authors()
    fig_articles()
    fig_viz_pieces()
    fig_corpus_overview()
    fig_pbn_reminder()
    print("wrote 5 figures to", HERE)
