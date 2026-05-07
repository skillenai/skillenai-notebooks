"""Compute three new per-skill signals across the full 222-skill universe:

- supply_demand_ratio: (technical-filtered blog count) / (job posting count)
                      via match_phrase on extractedText
- mean_idf:           mean per-document IDF, averaged across top-30
                      technical-filtered blog matches per skill
- hhi:                Herfindahl-Hirschman Index on companyCanonicalName
                      for per-skill postings in jobs_target_roles_canonical.csv

S/D and IDF reuse a single API call per index per skill (count + top-30
docs together via size=30, track_total_hits).

Outputs signal_supply_demand.csv, signal_idf.csv, signal_hhi.csv.
"""
import csv
import json
import math
import os
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

API_URL = "https://api.skillenai.com"
API_KEY = os.environ["API_KEY"]
HERE = Path(__file__).parent
SLEEP = 2.5

TECHNICAL_TOPICS = [
    "machine-learning", "deep-learning", "ml", "llm", "generative-ai", "mlops",
    "ai", "ai-coding-tools", "software-engineering", "devops", "backend",
    "cloud-computing", "data-science", "data-engineering", "python",
    "computer-vision", "nlp", "reinforcement-learning", "robotics", "agents",
    "security", "databases", "time-series", "speech-audio", "edge-ai",
    "open-source", "embedded", "graphics-3d", "compilers",
]

STOP = {
    "the", "and", "for", "are", "but", "not", "you", "all", "can", "her", "was",
    "one", "our", "out", "had", "his", "him", "she", "they", "their", "them",
    "this", "that", "these", "those", "with", "from", "have", "has", "been",
    "will", "would", "should", "could", "what", "when", "where", "which", "who",
    "why", "how", "may", "any", "some", "more", "most", "other", "such", "into",
    "than", "then", "also", "just", "only", "very", "much", "many", "make",
    "made", "use", "used", "using", "uses", "able", "well", "even", "way",
    "ways", "new", "see", "get", "got", "yes", "your", "its", "do", "does",
    "did", "doing", "done", "now", "two", "three", "first", "last", "after",
    "before", "between", "while", "during", "without", "across", "over",
    "under", "above", "below", "i", "we", "my", "me", "us", "or", "if", "an",
    "is", "as", "be", "to", "of", "in", "on", "at", "by", "it", "no", "so",
}
TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")


def tokenize(text):
    return [t.lower() for t in TOK.findall(text or "") if t.lower() not in STOP]


def search(body, max_retries=6):
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(8 * (2 ** attempt))
            else:
                raise


def load_idf():
    cache = HERE / "tfidf_corpus.json"
    if not cache.exists():
        raise SystemExit("tfidf_corpus.json missing; run eda_tfidf.py first")
    d = json.loads(cache.read_text())
    return d["n_docs"], d["idf"]


def fetch_blog(skill):
    body = {
        "indices": ["prod-enriched-blog"],
        "query": {
            "size": 30,
            "track_total_hits": True,
            "query": {"bool": {
                "must": [{"match_phrase": {"extractedText": skill}}],
                "filter": [{"terms": {"topics": TECHNICAL_TOPICS}}],
            }},
            "_source": ["extractedText"],
        },
    }
    return search(body)


def fetch_job_count(skill):
    body = {
        "indices": ["prod-enriched-jobs"],
        "query": {
            "size": 0,
            "track_total_hits": True,
            "query": {"match_phrase": {"extractedText": skill}},
        },
    }
    return search(body).get("total", 0)


def compute_idf_doc(text, idf, fallback):
    tokens = tokenize(text)
    if len(tokens) < 50:
        return None
    vals = [idf.get(t, fallback) for t in tokens]
    return sum(vals) / len(vals)


def universe_skills():
    u = json.loads((HERE / "canonical_universe.json").read_text())
    return [s["name"] for s in u["skills"]]


def compute_hhi():
    """Compute employer concentration metrics from local jobs CSV.

    Excludes Amazon postings — Amazon's recruiter-side JD template tags an
    enormous boilerplate skill list ('algorithms and data structures',
    'unix/linux', 'parallel and distributed computing', 'numerical
    optimization', 'mxnet') across most of their AI/ML postings, producing
    fake near-100% concentration on terms that are otherwise generic.
    Same artifact already caveats the Applied Scientist role bucket.
    """
    rows = list(csv.DictReader(open(HERE / "jobs_target_roles_canonical.csv")))
    per_skill = {}
    for r in rows:
        company = (r.get("companyCanonicalName") or "").strip()
        if not company or company.lower() == "amazon":
            continue
        for s in (r.get("canonical_skills") or "").split("|"):
            if s:
                per_skill.setdefault(s, Counter())[company] += 1

    out_rows = []
    for skill, counter in per_skill.items():
        n_jobs = sum(counter.values())
        n_emp = len(counter)
        if n_jobs < 30:  # was 10; raised to filter small-N HHI artifacts
            continue
        sorted_c = counter.most_common()
        top5 = sum(c for _, c in sorted_c[:5])
        hhi = sum((c / n_jobs) ** 2 for _, c in sorted_c)
        top1_name, top1_n = sorted_c[0]
        out_rows.append({
            "canonical_skill": skill,
            "n_jobs": n_jobs,
            "n_employers": n_emp,
            "top5_share": round(100 * top5 / n_jobs, 2),
            "hhi": round(hhi, 5),
            "top1_employer": top1_name,
            "top1_share": round(100 * top1_n / n_jobs, 2),
        })
    out_rows.sort(key=lambda r: -r["hhi"])
    fields = ["canonical_skill", "n_jobs", "n_employers", "top5_share", "hhi",
              "top1_employer", "top1_share"]
    with open(HERE / "signal_hhi.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote signal_hhi.csv: {len(out_rows)} skills (N>=10 postings)",
          file=sys.stderr)


def compute_blog_signals():
    """Compute S/D and mean-IDF together (one blog query + one job query per skill)."""
    skills = universe_skills()
    n_corpus, idf = load_idf()
    fallback = math.log(n_corpus / 2)

    sd_path = HERE / "signal_supply_demand.csv"
    idf_path = HERE / "signal_idf.csv"
    sd_done = {}
    idf_done = {}
    if sd_path.exists():
        for r in csv.DictReader(open(sd_path)):
            sd_done[r["canonical_skill"]] = r
    if idf_path.exists():
        for r in csv.DictReader(open(idf_path)):
            idf_done[r["canonical_skill"]] = r
    todo = [s for s in skills if s not in sd_done or s not in idf_done]
    print(f"Resuming with {len(sd_done)} S/D + {len(idf_done)} IDF done; "
          f"{len(todo)} todo (~{len(todo) * SLEEP * 2 / 60:.1f} min)",
          file=sys.stderr, flush=True)

    sd_rows = list(sd_done.values())
    idf_rows = list(idf_done.values())

    for i, skill in enumerate(todo, 1):
        try:
            blog = fetch_blog(skill)
            time.sleep(SLEEP)
            jobs = fetch_job_count(skill)
            time.sleep(SLEEP)
        except Exception as e:
            print(f"  ERR {skill}: {e}", file=sys.stderr)
            continue

        blog_count = blog.get("total", 0)
        job_count = jobs
        sd_ratio = blog_count / job_count if job_count > 0 else None
        sd_log = math.log10(sd_ratio) if sd_ratio and sd_ratio > 0 else None
        sd_rows.append({
            "canonical_skill": skill,
            "blog_count_technical": blog_count,
            "job_count": job_count,
            "sd_ratio": round(sd_ratio, 4) if sd_ratio is not None else "",
            "sd_log10": round(sd_log, 4) if sd_log is not None else "",
        })

        # IDF per doc
        per_doc = []
        for h in blog.get("hits", []):
            v = compute_idf_doc(h.get("extractedText", ""), idf, fallback)
            if v is not None:
                per_doc.append(v)
        if per_doc:
            per_doc.sort()
            n = len(per_doc)
            idf_rows.append({
                "canonical_skill": skill,
                "n_docs_used": n,
                "n_docs_total": blog_count,
                "mean_idf_p50": round(per_doc[n // 2], 4),
                "mean_idf_avg": round(sum(per_doc) / n, 4),
            })
        else:
            idf_rows.append({
                "canonical_skill": skill,
                "n_docs_used": 0,
                "n_docs_total": blog_count,
                "mean_idf_p50": "",
                "mean_idf_avg": "",
            })

        if i % 10 == 0 or i == len(todo):
            with open(sd_path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(sd_rows[0].keys()))
                w.writeheader(); w.writerows(sd_rows)
            with open(idf_path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(idf_rows[0].keys()))
                w.writeheader(); w.writerows(idf_rows)
            sd_str = f"{sd_ratio:.3f}" if sd_ratio is not None else "inf"
            print(f"  [{i}/{len(todo)}] {skill:30s} blog={blog_count:>5d} jobs={job_count:>5d} "
                  f"S/D={sd_str}",
                  file=sys.stderr, flush=True)

    print(f"Wrote {len(sd_rows)} S/D rows, {len(idf_rows)} IDF rows", file=sys.stderr)


def main():
    print("Step 1: HHI from local jobs CSV", file=sys.stderr)
    compute_hhi()
    print("\nStep 2: S/D + mean-IDF from API", file=sys.stderr)
    compute_blog_signals()


if __name__ == "__main__":
    main()
