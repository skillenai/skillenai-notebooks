"""EDA for blog-complexity difficulty metric.

For each candidate skill, pull ~30 blog docs filtered to technical topics,
compute candidate metrics, and print a comparison table. Goal: find metrics
that differentiate engineering-hard (JAX, kubernetes, distributed training)
from research-hard (transformer, fine-tuning, diffusion models) from easy
(prompt engineering, react, sql).
"""
import json
import os
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

API_URL = "https://api.skillenai.com"
API_KEY = os.environ["API_KEY"]

# Technical-topic allowlist (filter out non-technical content)
TECHNICAL_TOPICS = {
    "machine-learning", "deep-learning", "ml", "llm", "generative-ai", "mlops",
    "ai", "ai-coding-tools", "software-engineering", "devops", "backend",
    "cloud-computing", "data-science", "data-engineering", "python",
    "computer-vision", "nlp", "reinforcement-learning", "robotics", "agents",
    "security", "databases", "time-series", "speech-audio", "edge-ai",
    "open-source", "embedded", "graphics-3d", "compilers",
}

CANDIDATE_SKILLS = [
    ("JAX", "engineering"),
    ("Kubernetes", "engineering"),
    ("distributed training", "engineering"),
    ("CUDA", "engineering"),
    ("transformer", "research"),
    ("fine-tuning", "research"),
    ("diffusion models", "research"),
    ("reinforcement learning", "research"),
    ("prompt engineering", "easy/AIE"),
    ("React", "easy/frontend"),
    ("SQL", "easy/data"),
    ("agentic workflows", "AIE-hard"),
    ("RAG", "AIE-medium"),
]

# Math/Greek/symbolic glyphs that survive plain-text extraction
MATH_GLYPHS = set("∑∏∫∂∇√∞≈≠≤≥±×÷∈∉∧∨¬∀∃αβγδεζηθικλμνξπρστυφχψω∆ΩΣΠΦΨΘΛΞΓ←→↔⇒⇔")


def search(skill, n=30):
    body = {
        "indices": ["prod-enriched-blog"],
        "query": {
            "size": n,
            "track_total_hits": True,
            "query": {
                "bool": {
                    "must": [{"match_phrase": {"extractedText": skill}}],
                    "filter": [{"terms": {"topics": list(TECHNICAL_TOPICS)}}],
                },
            },
            "_source": ["title", "domain", "extractedText", "topics", "tags"],
        },
    }
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < 4:
                time.sleep(8 * (2 ** attempt))
            else:
                raise


def doc_metrics(text):
    if not text:
        return None
    words = text.split()
    n_words = len(words)
    if n_words < 50:
        return None
    n_chars = len(text)
    n_lines = text.count("\n")
    # Type-token ratio (lexical diversity): unique stems / total words.
    # Use a quick lowercase fold — not a real lemmatizer but adequate for ranking.
    lower = [w.lower().strip(".,;:!?\"'()[]{}") for w in words]
    n_unique = len(set(lower))
    ttr = n_unique / n_words if n_words else 0
    # Math-glyph density per 1000 words
    n_math = sum(text.count(g) for g in MATH_GLYPHS)
    math_per_1k = 1000 * n_math / n_words if n_words else 0
    # Numeric / equation-like density (digit-heavy passages signal technical content)
    n_digits = sum(c.isdigit() for c in text)
    digit_pct = 100 * n_digits / n_chars if n_chars else 0
    # Sentence length proxy — long sentences signal technical complexity
    sentences = re.split(r"[.!?]+\s", text)
    sentences = [s for s in sentences if s.strip()]
    avg_sent_len = n_words / len(sentences) if sentences else 0
    return {
        "n_words": n_words,
        "n_chars": n_chars,
        "ttr": ttr,
        "math_per_1k": math_per_1k,
        "digit_pct": digit_pct,
        "avg_sent_len": avg_sent_len,
        "n_lines": n_lines,
    }


def aggregate(skill, hits):
    metrics = [doc_metrics(h.get("extractedText", "")) for h in hits]
    metrics = [m for m in metrics if m]
    if not metrics:
        return None
    n = len(metrics)
    out = {"n_docs": n}
    for k in ["n_words", "ttr", "math_per_1k", "digit_pct", "avg_sent_len"]:
        vals = sorted(m[k] for m in metrics)
        out[k + "_mean"] = sum(vals) / n
        out[k + "_p50"] = vals[n // 2]
        out[k + "_p90"] = vals[min(n - 1, int(n * 0.9))]
    out["max_words"] = max(m["n_words"] for m in metrics)
    return out


def main():
    print(f"{'Skill':25s} {'class':14s} {'n':>4s}  {'words(p50)':>10s} {'words(p90)':>10s} {'words(max)':>10s} {'ttr(p50)':>9s} {'math/1k(p90)':>13s} {'avg_sent':>9s} {'digits%':>8s}")
    print("=" * 130)
    for skill, klass in CANDIDATE_SKILLS:
        try:
            r = search(skill)
            hits = r.get("hits", [])
            agg = aggregate(skill, hits)
        except Exception as e:
            print(f"{skill:25s} {klass:14s} ERROR: {e}")
            continue
        if not agg:
            print(f"{skill:25s} {klass:14s} (no usable docs)")
            continue
        print(f"{skill:25s} {klass:14s} {agg['n_docs']:>4d}  "
              f"{agg['n_words_p50']:>10.0f} {agg['n_words_p90']:>10.0f} {agg['max_words']:>10.0f}  "
              f"{agg['ttr_p50']:>9.3f} {agg['math_per_1k_p90']:>13.2f}  "
              f"{agg['avg_sent_len_p50']:>9.1f} {agg['digit_pct_p50']:>8.2f}")
        time.sleep(2.5)  # rate limit


if __name__ == "__main__":
    main()
