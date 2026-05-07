"""EDA: per-skill supply (technical blog count) vs demand (job posting count).

Supply  = match_phrase(extractedText) in prod-enriched-blog, filtered to docs
          with at least one technical topic. Proxy for "how many people are
          writing about this."
Demand  = match_phrase(extractedText) in prod-enriched-jobs. Proxy for "how
          many employers need this."

Ratio S/D, log(S/D), and percentile rank are candidate difficulty signals.
Low S/D = high demand relative to supply = scarce skill = harder.
"""
import json
import math
import os
import sys
import time
import urllib.request

API_URL = "https://api.skillenai.com"
API_KEY = os.environ["API_KEY"]
SLEEP = 5.0  # gentler than 9s; we're sequential not parallel

TECHNICAL_TOPICS = [
    "machine-learning", "deep-learning", "ml", "llm", "generative-ai", "mlops",
    "ai", "ai-coding-tools", "software-engineering", "devops", "backend",
    "cloud-computing", "data-science", "data-engineering", "python",
    "computer-vision", "nlp", "reinforcement-learning", "robotics", "agents",
    "security", "databases", "time-series", "speech-audio", "edge-ai",
    "open-source", "embedded", "graphics-3d", "compilers",
]

CANDIDATE_SKILLS = [
    ("JAX", "engineering"),
    ("Kubernetes", "engineering"),
    ("distributed training", "engineering"),
    ("CUDA", "engineering"),
    ("Terraform", "engineering"),
    ("FSDP", "engineering"),
    ("Triton", "engineering"),
    ("transformer", "research"),
    ("fine-tuning", "research"),
    ("diffusion models", "research"),
    ("reinforcement learning", "research"),
    ("RLHF", "research"),
    ("prompt engineering", "easy/AIE"),
    ("React", "easy/frontend"),
    ("SQL", "easy/data"),
    ("Python", "easy/baseline"),
    ("agentic workflows", "AIE-hard"),
    ("RAG", "AIE-medium"),
    ("LangChain", "AIE-easy"),
    ("vector databases", "AIE-medium"),
]


def query_count(index, phrase, technical_filter=False):
    must = [{"match_phrase": {"extractedText": phrase}}]
    body = {
        "indices": [index],
        "query": {"size": 0, "track_total_hits": True,
                  "query": {"bool": {"must": must}}},
    }
    if technical_filter:
        body["query"]["query"]["bool"]["filter"] = [
            {"terms": {"topics": TECHNICAL_TOPICS}},
        ]
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read()).get("total", 0)
        except Exception as e:
            if attempt < 5:
                time.sleep(8 * (2 ** attempt))
            else:
                raise


def main():
    print(f"{'Skill':25s} {'class':14s} {'blog_tech':>10s} {'jobs':>8s} {'S/D':>10s} {'log(S/D)':>10s}")
    print("=" * 90)
    rows = []
    for skill, klass in CANDIDATE_SKILLS:
        try:
            blog = query_count("prod-enriched-blog", skill, technical_filter=True)
            time.sleep(SLEEP)
            jobs = query_count("prod-enriched-jobs", skill)
            time.sleep(SLEEP)
        except Exception as e:
            print(f"{skill:25s}  ERROR: {e}")
            continue
        if jobs <= 0:
            ratio = float("inf")
            log_ratio = float("inf")
        else:
            ratio = blog / jobs
            log_ratio = math.log10(ratio) if ratio > 0 else -10
        rows.append((skill, klass, blog, jobs, ratio, log_ratio))
        print(f"{skill:25s} {klass:14s} {blog:>10d} {jobs:>8d} {ratio:>10.2f} {log_ratio:>10.2f}")

    print()
    print("Sorted by S/D ascending (lowest = scarcest = hardest by this metric):")
    for r in sorted(rows, key=lambda x: x[4]):
        print(f"  {r[0]:25s} {r[1]:14s} S/D={r[4]:>10.2f}")


if __name__ == "__main__":
    main()
