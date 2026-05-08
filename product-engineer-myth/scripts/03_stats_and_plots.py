"""Statistical validation + visualizations for PM / SWE / PE skill comparison.

Approach:
- Build the union of top-30 skills across the three roles (after canonicalization).
- For each skill: 3x2 chi-square (one role vs other two combined) on (has_skill, no_skill) counts.
- Bonferroni threshold = 0.05 / N_skills.
- Effect size: Cramer's V per skill.
- Then plot:
  1. Heatmap of prevalence across roles (top union)
  2. Bar chart of Jaccard pairwise overlaps
  3. Venn-style stacked bar showing PE composition
  4. PE-only / PM-only / SWE-only top skills side-by-side
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).parent
TOTALS = {"Product Manager": 7411, "Software Engineer": 26990, "Product Engineer": 666}

ALIAS_MAP = {
    "typescript": "TypeScript", "javascript": "JavaScript", "python": "Python",
    "react": "React", "reactjs": "React", "react.js": "React",
    "node.js": "Node.js", "nodejs": "Node.js",
    "next.js": "Next.js", "nextjs": "Next.js",
    "postgresql": "Postgres", "postgres": "Postgres",
    "amazon web services": "AWS", "amazon web services (aws)": "AWS", "aws": "AWS",
    "google cloud platform": "GCP", "gcp": "GCP",
    "graphql": "GraphQL",
    "ci/cd": "CI/CD", "ci-cd": "CI/CD",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes",
    "docker": "Docker",
    "machine learning": "Machine learning", "ml": "Machine learning",
    "ai": "AI", "artificial intelligence": "AI",
    "llm": "LLM", "llms": "LLM", "large language models": "LLM",
    "large language models (llm)": "LLM", "large language models (llms)": "LLM",
    "rest apis": "REST APIs", "rest api": "REST APIs",
    "restful apis": "REST APIs", "restful api": "REST APIs",
    "user research": "User research",
    "ab testing": "A/B testing", "a/b testing": "A/B testing",
    "data analysis": "Data analysis", "data analytics": "Data analysis",
    "product management": "Product management",
    "product strategy": "Product strategy",
    "product roadmap": "Product roadmap", "roadmap planning": "Product roadmap",
    "stakeholder management": "Stakeholder management",
    "stakeholder engagement": "Stakeholder management",
    "go-to-market": "Go-to-market", "go to market": "Go-to-market", "gtm": "Go-to-market",
    "user experience": "UX", "ux": "UX", "ui/ux": "UX",
    "user interface": "UI", "ui": "UI",
    "agile methodology": "Agile", "agile methodologies": "Agile", "agile": "Agile",
    "scrum": "Scrum",
    "system design": "System design", "distributed systems": "Distributed systems",
    "microservices": "Microservices",
    "cloud computing": "Cloud", "cloud": "Cloud",
    "cross-functional collaboration": "Cross-functional collaboration",
    "cross functional collaboration": "Cross-functional collaboration",
    "data-driven decision making": "Data-driven decisions",
    "data driven decision making": "Data-driven decisions",
    "data driven": "Data-driven decisions", "data-driven": "Data-driven decisions",
    "kpis": "KPIs", "kpi": "KPIs", "okrs": "OKRs", "okr": "OKRs",
}


def canon(name: str) -> str:
    return ALIAS_MAP.get(name.strip().lower(), name.strip())


def load_role_skills() -> dict[str, dict[str, int]]:
    raw = json.loads((ROOT / "role_skills.json").read_text())
    out: dict[str, dict[str, int]] = {}
    for role, items in raw.items():
        bucket: dict[str, int] = defaultdict(int)
        for item in items:
            bucket[canon(item["skill"])] += item["mentions"]
        out[role] = dict(bucket)
    return out


def chi2_2x2(a: int, b: int, c: int, d: int) -> tuple[float, float, float]:
    """2x2 chi-square with Yates correction. Returns (chi2, p, cramers_v).

    Table:        has_skill   no_skill
       focal        a           b
       other        c           d
    """
    n = a + b + c + d
    if n == 0:
        return 0.0, 1.0, 0.0
    # Expected
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    if row1 == 0 or row2 == 0 or col1 == 0 or col2 == 0:
        return 0.0, 1.0, 0.0
    e_a = row1 * col1 / n
    e_b = row1 * col2 / n
    e_c = row2 * col1 / n
    e_d = row2 * col2 / n
    # Yates
    chi2 = sum(
        (max(0, abs(o - e) - 0.5) ** 2) / e
        for o, e in [(a, e_a), (b, e_b), (c, e_c), (d, e_d)]
    )
    # Survival of chi2 with 1 df: p = erfc(sqrt(chi2/2))
    p = math.erfc(math.sqrt(chi2 / 2))
    # Cramer's V for 2x2 reduces to phi
    v = math.sqrt(chi2 / n)
    return chi2, p, v


def main() -> None:
    raw = load_role_skills()
    prev = {role: {s: c / TOTALS[role] for s, c in skills.items()} for role, skills in raw.items()}

    # Union of top 30 by prevalence per role
    top_per_role = {
        role: [s for s, _ in sorted(p.items(), key=lambda kv: -kv[1])[:30]]
        for role, p in prev.items()
    }
    union = sorted(set().union(*top_per_role.values()))
    print(f"Union of top-30 skills across roles: {len(union)}")

    # 3xN matrix prevalence
    matrix = np.zeros((3, len(union)))
    role_order = ["Product Manager", "Software Engineer", "Product Engineer"]
    for i, role in enumerate(role_order):
        for j, s in enumerate(union):
            matrix[i, j] = prev[role].get(s, 0.0)

    # ----- Chi-square per skill: PE vs (PM+SWE) -----
    rows = []
    bonf_n = len(union)
    for s in union:
        # raw counts (note: mentions ≈ unique-job counts but slight overcount possible)
        a = raw["Product Engineer"].get(s, 0)
        b = TOTALS["Product Engineer"] - a
        c = raw["Product Manager"].get(s, 0) + raw["Software Engineer"].get(s, 0)
        d = TOTALS["Product Manager"] + TOTALS["Software Engineer"] - c
        chi2, p, v = chi2_2x2(a, b, c, d)
        rows.append((s, a, c, prev["Product Engineer"].get(s,0), prev["Product Manager"].get(s,0), prev["Software Engineer"].get(s,0), chi2, p, v))

    print(f"\nChi-square per skill (PE vs PM+SWE) — Bonferroni α = 0.05/{bonf_n} = {0.05/bonf_n:.5f}")
    print(f"{'skill':<35}{'PE_pct':>8}{'PM_pct':>8}{'SWE_pct':>8}{'chi2':>10}{'p':>12}{'V':>8}")
    rows.sort(key=lambda r: -r[6])
    for r in rows[:20]:
        s, a, c, pe_p, pm_p, swe_p, chi2, p, v = r
        sig = "**" if p < 0.05 / bonf_n else ("*" if p < 0.05 else "")
        print(f"{s:<35}{pe_p*100:>7.1f}%{pm_p*100:>7.1f}%{swe_p*100:>7.1f}%{chi2:>10.1f}{p:>12.2e}{v:>8.3f}{sig}")

    # Save chi-square table
    with (ROOT / "pe_vs_others_chi2.csv").open("w") as f:
        f.write("skill,PE_count,Other_count,PE_pct,PM_pct,SWE_pct,chi2,p_value,cramers_v\n")
        for r in rows:
            s, a, c, pe_p, pm_p, swe_p, chi2, p, v = r
            f.write(f"{s},{a},{c},{pe_p:.4f},{pm_p:.4f},{swe_p:.4f},{chi2:.2f},{p:.4e},{v:.4f}\n")

    # ----- Plot 1: heatmap of prevalence -----
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, max(6, len(union) * 0.3)))
    cmap = LinearSegmentedColormap.from_list("blue_orange", ["#f7f7f7", "#3182bd"])
    # rank skills for visual: by max prevalence across roles
    ranking = sorted(range(len(union)), key=lambda j: -matrix[:, j].max())
    union_sorted = [union[j] for j in ranking]
    matrix_sorted = matrix[:, ranking]
    im = ax.imshow(matrix_sorted.T * 100, aspect="auto", cmap=cmap, vmin=0, vmax=50)
    ax.set_yticks(range(len(union_sorted)))
    ax.set_yticklabels(union_sorted)
    ax.set_xticks(range(3))
    ax.set_xticklabels(role_order)
    for i in range(3):
        for j in range(len(union_sorted)):
            v = matrix_sorted[i, j] * 100
            ax.text(i, j, f"{v:.0f}" if v >= 1 else "", ha="center", va="center",
                    fontsize=8, color="white" if v > 25 else "black")
    cbar = plt.colorbar(im, ax=ax, fraction=0.04)
    cbar.set_label("% of postings mentioning skill")
    ax.set_title("Top-30 skill prevalence (union across PM, SWE, Product Engineer)")
    plt.tight_layout()
    plt.savefig(ROOT / "01_heatmap.png", dpi=150)
    plt.close()
    print("Wrote 01_heatmap.png")

    # ----- Plot 2: Jaccard comparison + Venn-style PE composition -----
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    # Jaccard (top-50 ≥5% from earlier — recompute)
    def top_set(p, k=50, t=0.05):
        return {s for s, v in sorted(p.items(), key=lambda kv: -kv[1])[:k] if v >= t}
    sets = {r: top_set(prev[r]) for r in role_order}
    pairs = [("Product Manager", "Software Engineer"),
             ("Product Manager", "Product Engineer"),
             ("Software Engineer", "Product Engineer")]
    js = []
    labels = []
    for a, b in pairs:
        j = len(sets[a] & sets[b]) / len(sets[a] | sets[b]) if (sets[a] | sets[b]) else 0
        js.append(j)
        labels.append(f"{a.replace('Product ','').replace('Software ','SW ')}\n×\n{b.replace('Product ','').replace('Software ','SW ')}")
    ax0 = axes[0]
    bars = ax0.bar(labels, js, color=["#9ecae1", "#fdae6b", "#3182bd"])
    for bar, j in zip(bars, js):
        ax0.text(bar.get_x() + bar.get_width()/2, j + 0.01, f"{j:.2f}",
                 ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax0.set_ylabel("Jaccard similarity (top-50 skills, ≥5% prevalence)")
    ax0.set_ylim(0, max(js) * 1.3)
    ax0.set_title("Pairwise skill-set overlap")
    ax0.spines[["top","right"]].set_visible(False)

    # Venn-style breakdown of PE
    ax1 = axes[1]
    pe = sets["Product Engineer"]; pm = sets["Product Manager"]; swe = sets["Software Engineer"]
    pe_swe_only = pe & swe - pm
    pe_pm_only = pe & pm - swe
    pe_both = pe & swe & pm
    pe_neither = pe - swe - pm
    sizes = [len(pe_swe_only), len(pe_both), len(pe_pm_only), len(pe_neither)]
    cats = [f"In SWE only\n({len(pe_swe_only)})", f"In both PM&SWE\n({len(pe_both)})",
            f"In PM only\n({len(pe_pm_only)})", f"Unique to PE\n({len(pe_neither)})"]
    colors = ["#3182bd", "#756bb1", "#e6550d", "#31a354"]
    wedges, texts, autotexts = ax1.pie(sizes, labels=cats, autopct=lambda p: f"{p:.0f}%" if p > 3 else "",
                                       colors=colors, startangle=90, wedgeprops={"width": 0.4, "edgecolor": "white"})
    ax1.set_title(f"Composition of Product Engineer's top-{len(pe)} skill set")
    plt.tight_layout()
    plt.savefig(ROOT / "02_overlap.png", dpi=150)
    plt.close()
    print("Wrote 02_overlap.png")

    # ----- Plot 3: side-by-side asymmetric coverage -----
    swe_only_not_pe = sorted(swe - pe, key=lambda s: -prev["Software Engineer"][s])[:15]
    pm_only_not_pe = sorted(pm - pe, key=lambda s: -prev["Product Manager"][s])[:15]
    pe_unique = sorted(pe_neither, key=lambda s: -prev["Product Engineer"][s])[:15]

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    panels = [
        (axes[0], "SWE has but PE drops", swe_only_not_pe, "Software Engineer", "#3182bd"),
        (axes[1], "PM has but PE drops", pm_only_not_pe, "Product Manager", "#e6550d"),
        (axes[2], "Unique to Product Engineer", pe_unique, "Product Engineer", "#31a354"),
    ]
    for ax, title, skills, primary_role, color in panels:
        if not skills:
            ax.set_title(title + " (none)")
            ax.axis("off")
            continue
        skills = list(reversed(skills))
        x_primary = [prev[primary_role].get(s, 0) * 100 for s in skills]
        x_pe = [prev["Product Engineer"].get(s, 0) * 100 for s in skills]
        y = np.arange(len(skills))
        h = 0.4
        ax.barh(y - h/2, x_primary, h, color=color, label=primary_role)
        ax.barh(y + h/2, x_pe, h, color="#999", label="Product Engineer")
        for i, (a, b) in enumerate(zip(x_primary, x_pe)):
            ax.text(a + 0.4, i - h/2, f"{a:.0f}%", va="center", fontsize=8)
            ax.text(b + 0.4, i + h/2, f"{b:.0f}%", va="center", fontsize=8)
        ax.set_yticks(y)
        ax.set_yticklabels(skills)
        ax.set_xlabel("% of postings")
        ax.set_title(title)
        ax.legend(loc="lower right", fontsize=9)
        ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(ROOT / "03_asymmetric.png", dpi=150)
    plt.close()
    print("Wrote 03_asymmetric.png")

    # ----- Plot 4: PE vs SWE focused — what's the modern-stack tilt? -----
    # Build delta = PE_pct - SWE_pct, sort by absolute, take top 25
    deltas = []
    for s in union:
        d = prev["Product Engineer"].get(s, 0) - prev["Software Engineer"].get(s, 0)
        deltas.append((s, d, prev["Product Engineer"].get(s,0), prev["Software Engineer"].get(s,0)))
    deltas.sort(key=lambda r: r[1])
    bottom = deltas[:12]; top = deltas[-12:]
    show = bottom + top
    skills_ = [r[0] for r in show]
    vals_ = [r[1] * 100 for r in show]
    fig, ax = plt.subplots(figsize=(11, 8))
    colors_ = ["#3182bd" if v < 0 else "#31a354" for v in vals_]
    y = np.arange(len(skills_))
    ax.barh(y, vals_, color=colors_)
    ax.set_yticks(y)
    ax.set_yticklabels(skills_)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Prevalence delta: Product Engineer − Software Engineer (pp)")
    ax.set_title("Where Product Engineer diverges from Software Engineer\n(green = PE-leaning, blue = SWE-leaning)")
    for i, v in enumerate(vals_):
        ax.text(v + (0.4 if v >= 0 else -0.4), i, f"{v:+.0f}", va="center",
                ha="left" if v >= 0 else "right", fontsize=9)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(ROOT / "04_pe_vs_swe_delta.png", dpi=150)
    plt.close()
    print("Wrote 04_pe_vs_swe_delta.png")


if __name__ == "__main__":
    main()
