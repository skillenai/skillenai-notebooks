"""EDA: per-skill employer concentration from job postings.

Use the already-downloaded target-role jobs (8.7K postings across DS/MLE/AIE/
Research/Applied roles). For each candidate skill, count postings per company
and compute three concentration metrics:

- top5_share: fraction of postings at top-5 employers
- hhi: Herfindahl-Hirschman Index (sum of squared shares)
- n_employers: distinct companies posting

Hypothesis: specialist-hard skills concentrate at a handful of employers
(JAX → 5 frontier labs). Commodity skills spread across thousands.
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent

CANDIDATE_SKILLS = [
    ("jax", "engineering"),
    ("kubernetes", "engineering"),
    ("distributed training", "engineering"),
    ("cuda", "engineering"),
    ("terraform", "engineering"),
    ("fsdp", "engineering"),
    ("triton", "engineering"),
    ("transformer", "research"),
    ("fine-tuning", "research"),
    ("diffusion models", "research"),
    ("reinforcement learning", "research"),
    ("rlhf", "research"),
    ("reward modeling", "research"),
    ("sft", "research"),
    ("dpo", "research"),
    ("prompt engineering", "easy/AIE"),
    ("react", "easy/frontend"),
    ("sql", "easy/data"),
    ("python", "easy/baseline"),
    ("agentic workflows", "AIE-hard"),
    ("rag", "AIE-medium"),
    ("langchain", "AIE-easy"),
    ("vector databases", "AIE-medium"),
]


def main():
    rows = []
    with open(HERE / "jobs_target_roles_canonical.csv") as f:
        rows = list(csv.DictReader(f))

    # Build per-skill -> per-company posting count
    per_skill = {}
    for r in rows:
        company = (r.get("companyCanonicalName") or "").strip()
        if not company:
            continue
        skills = (r.get("canonical_skills") or "").split("|")
        for s in skills:
            if not s:
                continue
            per_skill.setdefault(s, Counter())
            per_skill[s][company] += 1

    print(f"{'Skill':25s} {'class':14s} {'n_jobs':>7s} {'n_emp':>7s} {'top5%':>7s} {'top10%':>7s} {'HHI':>7s} {'top1':>20s}")
    print("=" * 120)
    out = []
    for skill, klass in CANDIDATE_SKILLS:
        counter = per_skill.get(skill)
        if not counter:
            print(f"{skill:25s} {klass:14s} (no postings)")
            continue
        n_jobs = sum(counter.values())
        n_emp = len(counter)
        if n_jobs < 10:
            print(f"{skill:25s} {klass:14s} {n_jobs:>7d} {n_emp:>7d}  (N too small)")
            continue
        sorted_c = counter.most_common()
        top5 = sum(c for _, c in sorted_c[:5])
        top10 = sum(c for _, c in sorted_c[:10])
        # Herfindahl-Hirschman Index
        hhi = sum((c / n_jobs) ** 2 for _, c in sorted_c)
        top5_pct = 100 * top5 / n_jobs
        top10_pct = 100 * top10 / n_jobs
        top1_name = sorted_c[0][0]
        top1_share = sorted_c[0][1] / n_jobs * 100
        print(f"{skill:25s} {klass:14s} {n_jobs:>7d} {n_emp:>7d} {top5_pct:>6.1f}% {top10_pct:>6.1f}% {hhi:>7.3f} {top1_name[:18]:>18s} ({top1_share:.0f}%)")
        out.append((skill, klass, n_jobs, n_emp, top5_pct, top10_pct, hhi, top1_name))

    print("\nRanked by HHI descending (most concentrated = specialist):")
    for r in sorted(out, key=lambda x: -x[6]):
        print(f"  {r[0]:25s} {r[1]:14s} HHI={r[6]:.3f} top5={r[4]:.1f}% top1={r[7][:30]}")


if __name__ == "__main__":
    main()
