"""Figure generation for the FDE-as-new-SA analysis.

Inputs:  skill_counts.json (per-role concept prevalence)
Outputs: 01..05_*.png and stats.json
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

HERE = Path(__file__).parent
DATA = json.load(open(HERE / "skill_counts.json"))

ROLES = ["FDE", "AIE", "SA", "SWE"]
COLORS = {
    "FDE": "#E63946",   # red
    "AIE": "#F4A261",   # orange
    "SA":  "#2A9D8F",   # teal
    "SWE": "#264653",   # dark
}
TOTALS = {r: DATA[r]["total"] for r in ROLES}

# Concept grouping for the headline blend chart.
AI_PLATFORM = [
    ("LLMs",         "LLMs"),
    ("Agents",       "AI agents / agentic"),
    ("RAG",          "RAG"),
    ("Anthropic/Claude", "Anthropic / Claude"),
    ("OpenAI/GPT",   "OpenAI / GPT"),
    ("LangChain",    "LangChain"),
    ("Prompt eng",   "Prompt engineering"),
    ("Fine-tuning",  "Fine-tuning"),
    ("Production",   "Production AI"),
]
CUSTOMER_FACING = [
    ("Stakeholders", "Stakeholders"),
    ("Customer success", "Customer success"),
    ("Consulting",   "Consulting"),
    ("Communication","Communication"),
    ("Presales",     "Pre-sales"),
    ("Demos",        "Demos / POCs"),
    ("Travel",       "Travel required"),
]
HARDCORE_SWE = [
    ("Distributed systems", "Distributed systems"),
    ("Design patterns", "Design patterns"),
    ("Microservices", "Microservices"),
    ("System design", "System design"),
    ("Data structures", "DSA"),
]


def pct(role: str, concept: str) -> float:
    n = DATA[role]["counts"].get(concept, 0)
    t = TOTALS[role]
    return 100 * n / t if t else 0.0


def count(role: str, concept: str) -> int:
    return DATA[role]["counts"].get(concept, 0)


# ---------- FIGURE 1: The skill blend ----------

def fig_skill_blend() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 9), gridspec_kw={"width_ratios": [9, 7, 5]})
    panels = [
        (axes[0], "AI-platform skills",      "FDE ≈ AIE", AI_PLATFORM),
        (axes[1], "Customer-facing skills",  "FDE ≈ SA",  CUSTOMER_FACING),
        (axes[2], "Hardcore SWE skills",     "FDE ≈ AIE (both below SWE)", HARDCORE_SWE),
    ]
    for ax, title, subtitle, concepts in panels:
        ys = np.arange(len(concepts))
        bar_h = 0.2
        for i, role in enumerate(ROLES):
            offsets = bar_h * (1.5 - i)
            vals = [pct(role, c) for c, _ in concepts]
            ax.barh(ys + offsets, vals, height=bar_h, color=COLORS[role], label=role, edgecolor="white", linewidth=0.4)
        ax.set_yticks(ys)
        ax.set_yticklabels([label for _, label in concepts], fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel("% of postings mentioning skill")
        ax.set_title(title + "\n" + subtitle, fontsize=12, fontweight="bold")
        ax.grid(True, axis="x", linestyle=":", alpha=0.4)
        ax.set_axisbelow(True)
        max_x = max(pct(r, c) for r in ROLES for c, _ in concepts) * 1.1
        ax.set_xlim(0, max_x)
    axes[0].legend(loc="lower right", frameon=True, fontsize=10)
    fig.suptitle(
        "The FDE skill mix is literally AIE on the AI axis, SA on the customer axis",
        fontsize=14, fontweight="bold", y=0.995,
    )
    fig.text(0.5, 0.01,
        f"FDE n={TOTALS['FDE']:,}  ·  AIE n={TOTALS['AIE']:,}  ·  SA n={TOTALS['SA']:,}  ·  SWE n={TOTALS['SWE']:,}  ·  Skillenai prod-enriched-jobs, 2026-06-04",
        ha="center", fontsize=9, color="#555")
    fig.tight_layout(rect=[0, 0.02, 1, 0.97])
    fig.savefig(HERE / "01_skill_blend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- FIGURE 2: 5x customer-facing layer ----------

def fig_role_ratio_5x() -> None:
    fde_aie = TOTALS["FDE"] / TOTALS["AIE"] * 100
    sa_swe  = TOTALS["SA"]  / TOTALS["SWE"] * 100
    ratio = fde_aie / sa_swe

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar(
        ["AI era\nFDE / AI Engineer", "Cloud era\nSolutions Architect / Software Engineer"],
        [fde_aie, sa_swe],
        color=[COLORS["FDE"], COLORS["SA"]],
        edgecolor="white", linewidth=2,
    )
    for b, v in zip(bars, [fde_aie, sa_swe]):
        ax.text(b.get_x() + b.get_width()/2, v + 0.7, f"{v:.1f}%", ha="center", fontsize=14, fontweight="bold")
    ax.set_ylabel("Customer-facing role count as % of adjacent technical role")
    ax.set_ylim(0, max(fde_aie, sa_swe) * 1.18)
    ax.set_title(
        f"The customer-facing layer is {ratio:.1f}× thicker in AI than it was in cloud",
        fontsize=14, fontweight="bold",
    )
    ax.grid(True, axis="y", linestyle=":", alpha=0.4)
    ax.set_axisbelow(True)
    fig.text(0.5, 0.01,
        f"FDE n={TOTALS['FDE']:,}  ·  AIE n={TOTALS['AIE']:,}  ·  SA n={TOTALS['SA']:,}  ·  SWE n={TOTALS['SWE']:,}",
        ha="center", fontsize=9, color="#555")
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(HERE / "02_role_ratio_5x.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- FIGURE 3: Diffusion - top FDE employers ----------

# From the OpenSearch agg earlier (title="forward deployed engineer" OR "forward-deployed engineer")
TOP_EMPLOYERS = [
    ("Databricks", 30, False),
    ("Parloa", 25, False),
    ("OpenAI", 23, True),
    ("Workato", 23, False),
    ("Anthropic", 21, True),
    ("GitLab", 14, False),
    ("Truelogic", 14, False),
    ("Virtru", 12, False),
    ("Cohere", 11, True),
    ("Chalk", 16, False),       # 10 + 6 (chalkinc) duplicate slug
    ("Neara", 10, False),
    ("Intercom", 8, False),
    ("SonarSource", 7, False),
    ("hcompany", 7, True),
    ("Taktile", 6, False),
    ("UiPath", 6, False),
    ("Vercel", 6, False),
    ("Adobe", 5, False),
    ("AssemblyAI", 5, False),
    ("Cresta", 5, False),
]


def fig_diffusion_employers() -> None:
    rows = sorted(TOP_EMPLOYERS, key=lambda r: r[1], reverse=True)
    names = [r[0] for r in rows]
    counts = [r[1] for r in rows]
    frontier = [r[2] for r in rows]

    fig, ax = plt.subplots(figsize=(11, 8.5))
    colors = ["#9B2226" if f else "#94B3B6" for f in frontier]
    ys = np.arange(len(names))
    ax.barh(ys, counts, color=colors, edgecolor="white", linewidth=0.5)
    for y, n, c in zip(ys, names, counts):
        ax.text(c + 0.3, y, str(c), va="center", fontsize=10)
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Open FDE postings")
    ax.set_title(
        "The role has already diffused beyond frontier labs",
        fontsize=14, fontweight="bold",
    )
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(color="#9B2226", label="Frontier lab"),
        Patch(color="#94B3B6", label="Everyone else (enterprise SaaS + startups)"),
    ], loc="lower right", frameon=True, fontsize=10)
    ax.grid(True, axis="x", linestyle=":", alpha=0.4)
    ax.set_axisbelow(True)
    fig.text(0.5, 0.01,
        "Top 20 FDE employers by title-tagged posting count.  Skillenai prod-enriched-jobs, 2026-06-04.",
        ha="center", fontsize=9, color="#555")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(HERE / "03_diffusion_employers.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- FIGURE 4: Entry-share tier split ----------

# Frontier labs: OpenAI, Anthropic, Cohere, Mistral, xAI, Perplexity, hcompany, AI21, Reka, Inflection, Adept, Aleph Alpha
# Entry-share via role.keyword="Forward Deployed Engineer" (matches senior-club post's methodology):
#   Frontier (n=31 seniority-tagged): 2 entry → 6.5%
#   Other    (n=423 seniority-tagged): 61 entry → 14.4%
#   Overall FDE entry-share (role.keyword): 63 / 454 = 13.9%
FRONTIER_TAGGED = 31
FRONTIER_ENTRY  = 2
OTHER_TAGGED    = 423
OTHER_ENTRY     = 61
FRONTIER_PCT = 100 * FRONTIER_ENTRY / FRONTIER_TAGGED
OTHER_PCT    = 100 * OTHER_ENTRY    / OTHER_TAGGED
FDE_OVERALL_PCT = 13.9  # 63/454 via role.keyword

# From ai-labor-market-senior-club, 2026-06-03 baseline (per-role entry-share):
PEER_ROLES = [
    ("Data Analyst", 21.8, False),
    ("Software Engineer", 14.3, True),     # entry door
    ("Research Engineer", 14.0, False),
    ("Research Scientist", 13.0, False),
    ("Infrastructure Eng", 11.8, False),
    ("Frontend Eng", 10.8, False),
    ("Forward Deployed Eng (this post)", 13.9, True),
    ("Full Stack Eng", 10.5, False),
    ("AI Engineer", 10.4, False),
    ("Data Scientist", 7.8, False),
    ("DevOps Engineer", 7.6, False),
    ("Backend Engineer", 5.8, False),
    ("ML Engineer", 5.2, False),
    ("Platform Engineer", 2.9, False),
    ("Solutions Architect (this post)", 1.0, True),    # the cloud-era analog
]


def fig_entry_share() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [1, 1.4]})

    # ---- Left panel: tier split ----
    bars = ax1.bar(
        ["Frontier labs\n(OpenAI, Anthropic, Cohere, …)", "Everyone else\n(Databricks, Chalk, Workato, …)"],
        [FRONTIER_PCT, OTHER_PCT],
        color=["#9B2226", "#94B3B6"],
        edgecolor="white", linewidth=2,
    )
    for b, v, n_entry, n_tot in zip(bars, [FRONTIER_PCT, OTHER_PCT],
                                     [FRONTIER_ENTRY, OTHER_ENTRY],
                                     [FRONTIER_TAGGED, OTHER_TAGGED]):
        ax1.text(b.get_x()+b.get_width()/2, v+0.4, f"{v:.1f}%", ha="center", fontsize=15, fontweight="bold")
        ax1.text(b.get_x()+b.get_width()/2, v+1.7, f"({n_entry} / {n_tot})", ha="center", fontsize=10, color="#444")
    ax1.axhline(10, color="#333", linestyle="--", linewidth=1.2)
    ax1.text(1.42, 10.3, "10% entry-door line\n(from senior-club post, 06-03)", fontsize=9, color="#333")
    ax1.set_ylabel("Entry-share of FDE postings (%)")
    ax1.set_ylim(0, max(FRONTIER_PCT, OTHER_PCT)*1.35)
    ax1.set_title("Entry-share of FDE postings by employer tier", fontsize=13, fontweight="bold")
    ax1.grid(True, axis="y", linestyle=":", alpha=0.4)
    ax1.set_axisbelow(True)

    # ---- Right panel: FDE on yesterday's per-role entry-share ladder ----
    sorted_roles = sorted(PEER_ROLES, key=lambda r: r[1], reverse=True)
    names = [r[0] for r in sorted_roles]
    vals = [r[1] for r in sorted_roles]
    highlight = [r[2] for r in sorted_roles]
    colors = ["#E63946" if h else "#94B3B6" for h in highlight]
    ys = np.arange(len(names))
    ax2.barh(ys, vals, color=colors, edgecolor="white", linewidth=0.5)
    for y, v in zip(ys, vals):
        ax2.text(v + 0.3, y, f"{v:.1f}%", va="center", fontsize=9)
    ax2.set_yticks(ys)
    ax2.set_yticklabels(names, fontsize=10)
    ax2.invert_yaxis()
    ax2.axvline(10, color="#333", linestyle="--", linewidth=1.2)
    ax2.set_xlabel("Entry-share (%)")
    ax2.set_title("Where FDE sits on yesterday's role-entry ladder", fontsize=13, fontweight="bold")
    ax2.grid(True, axis="x", linestyle=":", alpha=0.4)
    ax2.set_axisbelow(True)

    fig.suptitle(
        "Frontier labs hire FDEs the way AWS hires SAs — senior-only.\n"
        "Everywhere else, \"FDE\" is being rebranded for entry-level customer engineering.",
        fontsize=14, fontweight="bold", y=1.02,
    )
    fig.text(0.5, 0.01,
        f"FDE n={TOTALS['FDE']:,} title-tagged postings ({FRONTIER_TAGGED + OTHER_TAGGED} with seniority tag).  "
        "Peer ladder from ai-labor-market-senior-club, 2026-06-03.",
        ha="center", fontsize=9, color="#555")
    fig.tight_layout(rect=[0, 0.02, 1, 0.97])
    fig.savefig(HERE / "04_entry_share_tier_split.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- STATS ----------

def chi2_2x2(a: int, n_a: int, b: int, n_b: int, label: str) -> dict:
    """2x2 chi-square: group A (a/n_a-a) vs group B (b/n_b-b)."""
    table = np.array([[a, n_a - a], [b, n_b - b]])
    chi2, p, dof, exp = stats.chi2_contingency(table, correction=False)
    return {
        "label": label,
        "a": a, "n_a": n_a, "p_a": a/n_a if n_a else 0,
        "b": b, "n_b": n_b, "p_b": b/n_b if n_b else 0,
        "chi2": chi2, "p_value": p,
    }


def run_stats() -> None:
    out = {}

    # 1. FDE vs AIE on AI-platform skills — expect H0 not strongly rejected (similar)
    for c, _ in AI_PLATFORM:
        out[f"FDE_vs_AIE__{c}"] = chi2_2x2(count("FDE", c), TOTALS["FDE"], count("AIE", c), TOTALS["AIE"],
                                            label=f"FDE vs AIE: {c}")

    # 2. FDE vs SA on customer-facing — expect H0 not strongly rejected (similar)
    for c, _ in CUSTOMER_FACING:
        out[f"FDE_vs_SA__{c}"] = chi2_2x2(count("FDE", c), TOTALS["FDE"], count("SA", c), TOTALS["SA"],
                                           label=f"FDE vs SA: {c}")

    # 3. FDE vs SWE on hardcore SWE — expect FDE significantly LOWER
    for c, _ in HARDCORE_SWE:
        out[f"FDE_vs_SWE__{c}"] = chi2_2x2(count("FDE", c), TOTALS["FDE"], count("SWE", c), TOTALS["SWE"],
                                            label=f"FDE vs SWE: {c}")

    # 4. Tier split entry-share (frontier vs other)
    out["tier_entry_share"] = chi2_2x2(FRONTIER_ENTRY, FRONTIER_TAGGED, OTHER_ENTRY, OTHER_TAGGED,
                                        label="Frontier vs Other: FDE entry-share")

    # Save
    json.dump(out, open(HERE / "stats.json", "w"), indent=2)
    print(f"wrote stats for {len(out)} tests")


if __name__ == "__main__":
    fig_skill_blend()
    fig_role_ratio_5x()
    fig_diffusion_employers()
    fig_entry_share()
    run_stats()
    print("done. figures + stats written to", HERE)
