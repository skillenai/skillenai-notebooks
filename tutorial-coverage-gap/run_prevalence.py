"""Per-index prevalence sweep with index-specific must_not filters.

Reads a concepts JSON (label -> phrase or list of phrases), runs a chunked
filters-aggregation on each (index, base_filter) pair, prints + writes JSON.
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from pathlib import Path

import requests

API_URL = "https://api.skillenai.com"
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]
FIELD = "extractedText"
CHUNK = 8
SLEEP = 1.9

CONCEPTS_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/concepts.json"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "/tmp/prevalence.json"

raw = json.loads(Path(CONCEPTS_PATH).read_text())
concepts: dict[str, list[str]] = {k: ([v] if isinstance(v, str) else list(v)) for k, v in raw.items()}

# --- PBN domain denylist for blog index ---
pbn_path = Path("/Users/jrand/git-repos/skillenai-notebooks/synthetic-breakout-may-2026/network_domains_seed.csv")
pbn_domains: list[str] = []
if pbn_path.exists():
    rdr = csv.reader(pbn_path.open())
    next(rdr)
    pbn_domains = [row[0].strip() for row in rdr if row and row[0].strip()]

# SKI-274 mis-tagged-as-blog noise domains
ski274_noise = [
    "search.jobs.barclays.com", "nofluffjobs.com",
    "vascularnews.com", "researchsquare.com", "lup.lub.lu.se",
]

blog_must_not = []
if pbn_domains:
    blog_must_not.append({"terms": {"domain": pbn_domains}})
if ski274_noise:
    blog_must_not.append({"terms": {"domain": ski274_noise}})

INDEX_FILTERS = {
    "prod-enriched-jobs": [],
    "prod-enriched-blog": blog_must_not,
}


def phrase_clause(phrases: list[str]) -> dict:
    if len(phrases) == 1:
        return {"match_phrase": {FIELD: phrases[0]}}
    return {"bool": {"should": [{"match_phrase": {FIELD: p}} for p in phrases], "minimum_should_match": 1}}


def base_query(must_not: list[dict]) -> dict:
    if not must_not:
        return {"match_all": {}}
    return {"bool": {"must": [{"match_all": {}}], "must_not": must_not}}


def search(body: dict, retries: int = 5, backoff: float = 10.0) -> dict:
    for attempt in range(retries):
        try:
            r = requests.post(
                f"{API_URL}/v1/query/search",
                headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
                json=body,
                timeout=60,
            )
            if r.status_code == 429:
                print(f"  429 — back off {backoff*(attempt+1)}s", file=sys.stderr)
                time.sleep(backoff * (attempt + 1))
                continue
            r.raise_for_status()
            d = r.json()
            if "aggregations" in d:
                return d
            print(f"  WARN: no aggregations in response: {json.dumps(d)[:200]}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"  request error (attempt {attempt+1}): {e}", file=sys.stderr)
        time.sleep(backoff)
    return {}


def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def run_index(index: str, must_not: list[dict]) -> tuple[int, dict[str, int]]:
    total = 0
    counts: dict[str, int] = {}
    bq = base_query(must_not)
    chunk_list = list(chunks(list(concepts.items()), CHUNK))
    for i, sub in enumerate(chunk_list):
        body = {
            "indices": [index],
            "query": {
                "size": 0,
                "track_total_hits": True,
                "query": bq,
                "aggs": {"concepts": {"filters": {"filters": {label: phrase_clause(ph) for label, ph in sub}}}},
            },
        }
        d = search(body)
        if not d:
            print(f"  {index} chunk {i+1}/{len(chunk_list)} EMPTY — skipping {[s[0] for s in sub]}", file=sys.stderr)
            continue
        total = d.get("total", total)
        for label, bucket in d["aggregations"]["concepts"]["buckets"].items():
            counts[label] = bucket["doc_count"]
        print(f"  {index} chunk {i+1}/{len(chunk_list)} ok ({len([s for s in sub])} concepts)", file=sys.stderr)
        time.sleep(SLEEP)
    return total, counts


out: dict[str, dict] = {"totals": {}, "results": {}}
for idx, mn in INDEX_FILTERS.items():
    print(f"\n=== {idx}  must_not_clauses={len(mn)} ===", file=sys.stderr)
    t, c = run_index(idx, mn)
    out["totals"][idx] = t
    out["results"][idx] = c
    print(f"  denominator={t:,}  concepts_resolved={len(c)}", file=sys.stderr)

Path(OUT_PATH).write_text(json.dumps(out, indent=2))
print(f"\nwrote {OUT_PATH}", file=sys.stderr)

# Print table
primary = "prod-enriched-jobs"
order = sorted(concepts.keys(), key=lambda n: -out["results"][primary].get(n, 0))
totals = out["totals"]
print(f"\n{'concept':30}  {'jobs':>9} {'jobs/10k':>9}  {'blog':>9} {'blog/10k':>9}  {'job:blog':>8}")
print("-" * 86)
for n in order:
    jc = out["results"][primary].get(n, 0)
    bc = out["results"]["prod-enriched-blog"].get(n, 0)
    jrate = jc / totals[primary] * 10000 if totals[primary] else 0.0
    brate = bc / totals["prod-enriched-blog"] * 10000 if totals["prod-enriched-blog"] else 0.0
    ratio = (jrate / brate) if brate > 0 else float("inf")
    print(f"{n:30}  {jc:>9,} {jrate:>9.1f}  {bc:>9,} {brate:>9.1f}  {ratio:>8.2f}")
print(f"\ndenominators: jobs={totals['prod-enriched-jobs']:,}  blog={totals['prod-enriched-blog']:,} (post-denylist)")
