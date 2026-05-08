"""Compute skill overlap between PM, SWE, and PE.

Strategy:
- Treat mentions/total as prevalence (jobs in this role mentioning the skill at least once).
  NER almost always emits a skill once per doc, so this is a tight upper bound.
- Light canonicalization: lowercase + obvious aliases.
- Top-K skill set per role; Jaccard, asymmetric coverage, PE-vs-SWE/PM tilt.
"""
from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict
import csv

ROOT = Path(__file__).parent
TOTALS = {"Product Manager": 7411, "Software Engineer": 26990, "Product Engineer": 666}

# Manual canonicalization map for the obvious duplicates surfaced in the data
ALIAS_MAP = {
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "python": "Python",
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "postgresql": "Postgres",
    "postgres": "Postgres",
    "amazon web services": "AWS",
    "amazon web services (aws)": "AWS",
    "aws": "AWS",
    "google cloud platform": "GCP",
    "gcp": "GCP",
    "graphql": "GraphQL",
    "ci/cd": "CI/CD",
    "ci-cd": "CI/CD",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "docker": "Docker",
    "machine learning": "Machine learning",
    "ml": "Machine learning",
    "ai": "AI",
    "artificial intelligence": "AI",
    "llm": "LLM",
    "llms": "LLM",
    "large language models": "LLM",
    "large language models (llm)": "LLM",
    "large language models (llms)": "LLM",
    "rest apis": "REST APIs",
    "rest api": "REST APIs",
    "restful apis": "REST APIs",
    "restful api": "REST APIs",
    "user research": "User research",
    "ab testing": "A/B testing",
    "a/b testing": "A/B testing",
    "data analysis": "Data analysis",
    "data analytics": "Data analysis",
    "product management": "Product management",
    "product strategy": "Product strategy",
    "product roadmap": "Product roadmap",
    "roadmap planning": "Product roadmap",
    "stakeholder management": "Stakeholder management",
    "stakeholder engagement": "Stakeholder management",
    "go-to-market": "Go-to-market",
    "go to market": "Go-to-market",
    "gtm": "Go-to-market",
    "user experience": "UX",
    "ux": "UX",
    "ui/ux": "UX",
    "user interface": "UI",
    "ui": "UI",
    "agile methodology": "Agile",
    "agile methodologies": "Agile",
    "agile": "Agile",
    "scrum": "Scrum",
    "system design": "System design",
    "distributed systems": "Distributed systems",
    "microservices": "Microservices",
    "cloud computing": "Cloud",
    "cloud": "Cloud",
    "cross-functional collaboration": "Cross-functional collaboration",
    "cross functional collaboration": "Cross-functional collaboration",
    "data-driven decision making": "Data-driven decisions",
    "data driven decision making": "Data-driven decisions",
    "data driven": "Data-driven decisions",
    "data-driven": "Data-driven decisions",
    "kpis": "KPIs",
    "kpi": "KPIs",
    "okrs": "OKRs",
    "okr": "OKRs",
}


def canon(name: str) -> str:
    n = name.strip()
    return ALIAS_MAP.get(n.lower(), n)


def load_role_skills() -> dict[str, dict[str, int]]:
    """Returns {role_label: {canonical_skill: prevalence_count}} after canonicalization."""
    raw = json.loads((ROOT / "role_skills.json").read_text())
    out: dict[str, dict[str, int]] = {}
    for role, items in raw.items():
        bucket: dict[str, int] = defaultdict(int)
        for item in items:
            bucket[canon(item["skill"])] += item["mentions"]
        out[role] = dict(bucket)
    return out


def prevalence(role_skills: dict[str, dict[str, int]]) -> dict[str, dict[str, float]]:
    """Convert mention counts → prevalence (fraction of postings)."""
    return {
        role: {s: c / TOTALS[role] for s, c in skills.items()}
        for role, skills in role_skills.items()
    }


def top_set(prev: dict[str, float], k: int = 50, threshold: float = 0.05) -> set[str]:
    """Top-K skills with prevalence above threshold."""
    items = sorted(prev.items(), key=lambda kv: -kv[1])
    return {s for s, p in items[:k] if p >= threshold}


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if (a or b) else 0.0


def main() -> None:
    raw = load_role_skills()
    prev = prevalence(raw)

    # Top-50 sets at ≥5% prevalence
    sets_50_5 = {role: top_set(p, k=50, threshold=0.05) for role, p in prev.items()}
    sets_30_5 = {role: top_set(p, k=30, threshold=0.05) for role, p in prev.items()}

    print("=== Top-50, prevalence ≥ 5% ===")
    for role, s in sets_50_5.items():
        print(f"  {role:<22} |set|={len(s)}")

    pairs = [
        ("Product Manager", "Software Engineer"),
        ("Product Manager", "Product Engineer"),
        ("Software Engineer", "Product Engineer"),
    ]
    print("\n=== Jaccard (top-50 ≥5%) ===")
    for a, b in pairs:
        j = jaccard(sets_50_5[a], sets_50_5[b])
        print(f"  {a} ∩ {b}: J={j:.3f}  shared={len(sets_50_5[a] & sets_50_5[b])}")

    pe = sets_50_5["Product Engineer"]
    pm = sets_50_5["Product Manager"]
    swe = sets_50_5["Software Engineer"]

    print("\n=== Where does Product Engineer sit? ===")
    pe_in_swe_only = pe & swe - pm
    pe_in_pm_only = pe & pm - swe
    pe_in_both = pe & swe & pm
    pe_in_neither = pe - swe - pm
    print(f"  PE skills in SWE-only: {len(pe_in_swe_only)}")
    print(f"  PE skills in PM-only:  {len(pe_in_pm_only)}")
    print(f"  PE skills in both:     {len(pe_in_both)}")
    print(f"  PE skills in neither:  {len(pe_in_neither)}")

    # Skills present in SWE & PM but NOT in PE — "true intersection" missed by PE
    intersection_missed_by_pe = (swe & pm) - pe
    print(f"\n  SWE∩PM skills NOT in PE: {len(intersection_missed_by_pe)}")
    for s in sorted(intersection_missed_by_pe):
        print(
            f"    {s:<35}  PE={prev['Product Engineer'].get(s,0):.2%}  SWE={prev['Software Engineer'].get(s,0):.2%}  PM={prev['Product Manager'].get(s,0):.2%}"
        )

    swe_minus_pe = swe - pe
    print(f"\n  SWE-only top skills NOT in PE (top 20): {len(swe_minus_pe)}")
    swe_only_sorted = sorted(swe_minus_pe, key=lambda s: -prev["Software Engineer"].get(s, 0))
    for s in swe_only_sorted[:20]:
        print(
            f"    {s:<35}  PE={prev['Product Engineer'].get(s,0):.2%}  SWE={prev['Software Engineer'].get(s,0):.2%}  PM={prev['Product Manager'].get(s,0):.2%}"
        )

    pm_minus_pe = pm - pe
    print(f"\n  PM-only top skills NOT in PE (top 20): {len(pm_minus_pe)}")
    pm_only_sorted = sorted(pm_minus_pe, key=lambda s: -prev["Product Manager"].get(s, 0))
    for s in pm_only_sorted[:20]:
        print(
            f"    {s:<35}  PE={prev['Product Engineer'].get(s,0):.2%}  SWE={prev['Software Engineer'].get(s,0):.2%}  PM={prev['Product Manager'].get(s,0):.2%}"
        )

    pe_only_sorted = sorted(pe_in_neither, key=lambda s: -prev["Product Engineer"].get(s, 0))
    print(f"\n  PE-only top skills (NOT in SWE or PM): {len(pe_in_neither)}")
    for s in pe_only_sorted[:20]:
        print(
            f"    {s:<35}  PE={prev['Product Engineer'].get(s,0):.2%}  SWE={prev['Software Engineer'].get(s,0):.2%}  PM={prev['Product Manager'].get(s,0):.2%}"
        )

    # Save full prevalence matrix as CSV
    all_skills = sorted(set().union(*(prev[r].keys() for r in prev)))
    out_csv = ROOT / "prevalence_matrix.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill", "PM_pct", "SWE_pct", "PE_pct"])
        for s in all_skills:
            w.writerow(
                [
                    s,
                    f"{prev['Product Manager'].get(s,0)*100:.2f}",
                    f"{prev['Software Engineer'].get(s,0)*100:.2f}",
                    f"{prev['Product Engineer'].get(s,0)*100:.2f}",
                ]
            )
    print(f"\nWrote {out_csv}")

    # Save the typed-set summary as JSON
    summary = {
        "totals": TOTALS,
        "pe_in_swe_only": sorted(pe_in_swe_only),
        "pe_in_pm_only": sorted(pe_in_pm_only),
        "pe_in_both": sorted(pe_in_both),
        "pe_in_neither": sorted(pe_in_neither),
        "intersection_missed_by_pe": sorted(intersection_missed_by_pe),
        "swe_only_not_in_pe": swe_only_sorted[:30],
        "pm_only_not_in_pe": pm_only_sorted[:30],
        "jaccard": {
            f"{a} vs {b}": jaccard(sets_50_5[a], sets_50_5[b]) for a, b in pairs
        },
    }
    (ROOT / "overlap_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"Wrote overlap_summary.json")


if __name__ == "__main__":
    main()
