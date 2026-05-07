"""EDA: per-skill rare-word density (mean IDF) from blog corpus.

1. Sample ~3000 technical-topic blog docs.
2. Tokenize (lowercase alpha tokens, length >= 3, drop stopwords) and build
   a corpus-wide IDF: idf(t) = log(N / (1 + df(t))).
3. For each candidate skill, fetch ~30 blog docs match_phrasing it and
   technical-topic-filtered. For each doc compute mean IDF over its tokens.
4. Aggregate per skill: median + p90 of per-doc mean IDF.

Hypothesis: skills whose articles use rarer technical jargon (high mean IDF)
are harder/more specialized than skills with common-vocabulary articles.
"""
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

CORPUS_SIZE = 3000
PAGE_SIZE = 100
PER_SKILL_DOCS = 30

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
    "made", "make", "use", "used", "using", "uses", "able", "well", "even",
    "way", "ways", "new", "see", "get", "got", "yes", "your", "its", "do",
    "does", "did", "doing", "done", "now", "two", "three", "first", "last",
    "after", "before", "between", "while", "during", "without", "across",
    "over", "under", "above", "below",
    "i", "we", "my", "me", "us", "or", "if", "an", "is", "as", "be", "to",
    "of", "in", "on", "at", "by", "it", "no", "so",
}

CANDIDATE_SKILLS = [
    ("JAX", "engineering"),
    ("Kubernetes", "engineering"),
    ("distributed training", "engineering"),
    ("CUDA", "engineering"),
    ("Terraform", "engineering"),
    ("transformer", "research"),
    ("fine-tuning", "research"),
    ("diffusion models", "research"),
    ("reinforcement learning", "research"),
    ("RLHF", "research"),
    ("prompt engineering", "easy/AIE"),
    ("React", "easy/frontend"),
    ("SQL", "easy/data"),
    ("agentic workflows", "AIE-hard"),
    ("RAG", "AIE-medium"),
    ("LangChain", "AIE-easy"),
    ("vector databases", "AIE-medium"),
]

TOK = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]{2,}")


def tokenize(text):
    return [t.lower() for t in TOK.findall(text or "") if t.lower() not in STOP]


def search(body):
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < 5:
                time.sleep(8 * (2 ** attempt))
            else:
                raise


def build_idf():
    """Sample CORPUS_SIZE technical-topic blog docs, build IDF model."""
    cache = Path(__file__).parent / "tfidf_corpus.json"
    if cache.exists():
        d = json.loads(cache.read_text())
        print(f"Loaded cached IDF: N={d['n_docs']}, vocab={len(d['idf'])}",
              file=sys.stderr)
        return d["n_docs"], d["idf"]

    print(f"Sampling up to {CORPUS_SIZE} technical-topic blog docs...",
          file=sys.stderr, flush=True)
    df = Counter()
    n_docs = 0
    n_pages = (CORPUS_SIZE + PAGE_SIZE - 1) // PAGE_SIZE
    for page in range(n_pages):
        body = {
            "indices": ["prod-enriched-blog"],
            "query": {
                "size": PAGE_SIZE,
                "from": page * PAGE_SIZE,
                "track_total_hits": True,
                "query": {"bool": {
                    "must": [{"match_all": {}}],
                    "filter": [{"terms": {"topics": TECHNICAL_TOPICS}}],
                }},
                "_source": ["extractedText"],
            },
        }
        resp = search(body)
        hits = resp.get("hits", [])
        if not hits:
            break
        for h in hits:
            tokens = set(tokenize(h.get("extractedText", "")))
            if len(tokens) < 30:
                continue
            for t in tokens:
                df[t] += 1
            n_docs += 1
        print(f"  page {page+1}/{n_pages}: cumulative {n_docs} docs, "
              f"{len(df)} terms", file=sys.stderr, flush=True)
        time.sleep(2.5)

    idf = {t: math.log(n_docs / (1 + dfval)) for t, dfval in df.items()
           if dfval >= 2}  # filter out singletons (typos)
    cache.write_text(json.dumps({"n_docs": n_docs, "idf": idf}))
    print(f"Built IDF: N={n_docs}, vocab={len(idf)} (after df>=2 filter)",
          file=sys.stderr)
    return n_docs, idf


def skill_metrics(skill, idf, n_corpus):
    body = {
        "indices": ["prod-enriched-blog"],
        "query": {
            "size": PER_SKILL_DOCS,
            "track_total_hits": True,
            "query": {"bool": {
                "must": [{"match_phrase": {"extractedText": skill}}],
                "filter": [{"terms": {"topics": TECHNICAL_TOPICS}}],
            }},
            "_source": ["extractedText"],
        },
    }
    resp = search(body)
    hits = resp.get("hits", [])
    n_total = resp.get("total", 0)
    per_doc = []
    for h in hits:
        tokens = tokenize(h.get("extractedText", ""))
        if len(tokens) < 50:
            continue
        idfs = [idf.get(t, math.log(n_corpus / 2)) for t in tokens]
        per_doc.append(sum(idfs) / len(idfs))
    if not per_doc:
        return None
    per_doc.sort()
    n = len(per_doc)
    return {
        "n_docs_total": n_total,
        "n_used": n,
        "mean_idf_p50": per_doc[n // 2],
        "mean_idf_p90": per_doc[min(n - 1, int(n * 0.9))],
        "mean_idf_avg": sum(per_doc) / n,
    }


def main():
    n_corpus, idf = build_idf()
    print(f"\n{'Skill':25s} {'class':14s} {'n_total':>7s} {'n_used':>6s} "
          f"{'idf_p50':>8s} {'idf_p90':>8s} {'idf_avg':>8s}")
    print("=" * 90)
    rows = []
    for skill, klass in CANDIDATE_SKILLS:
        try:
            m = skill_metrics(skill, idf, n_corpus)
        except Exception as e:
            print(f"{skill:25s} {klass:14s}  ERROR: {e}")
            continue
        if not m:
            print(f"{skill:25s} {klass:14s} (no usable docs)")
            continue
        rows.append((skill, klass, m))
        print(f"{skill:25s} {klass:14s} {m['n_docs_total']:>7d} {m['n_used']:>6d} "
              f"{m['mean_idf_p50']:>8.3f} {m['mean_idf_p90']:>8.3f} {m['mean_idf_avg']:>8.3f}")
        time.sleep(2.5)

    print("\nRanked by median per-doc mean-IDF (highest = jargon-heaviest):")
    for s, k, m in sorted(rows, key=lambda x: -x[2]["mean_idf_p50"]):
        print(f"  {s:25s} {k:14s} idf_p50={m['mean_idf_p50']:.3f}")


if __name__ == "__main__":
    main()
