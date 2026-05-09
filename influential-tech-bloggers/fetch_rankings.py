#!/usr/bin/env python3
"""Pull the three blogger rankings (volume, per-post authority, sum) with a
single richer aggregation. Saves raw + cleaned JSON for downstream plotting."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

API_KEY = os.environ.get("SKILLENAI_INSIGHTS_API_KEY")
API_URL = os.environ.get("API_URL", "https://api.skillenai.com")
INDEX = "prod-enriched-blog"

if not API_KEY:
    sys.exit("Missing SKILLENAI_INSIGHTS_API_KEY")

OUT = Path(__file__).parent
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def post(body: dict[str, Any], retries: int = 6) -> dict[str, Any]:
    for attempt in range(retries):
        r = requests.post(f"{API_URL}/v1/query/search", headers=HEADERS, json=body, timeout=60)
        try:
            j = r.json()
        except ValueError:
            time.sleep(8)
            continue
        if isinstance(j, dict) and j.get("error", {}).get("code") == "rate_limited":
            time.sleep(10 * (attempt + 1))
            continue
        return j
    raise RuntimeError("Persistent rate-limit / transient failure")


JUNK_AUTHOR_PATTERNS = [
    r"^$",
    r"^admin$",
    r"^Author$",
    r"^Unknown$",
    r"^Editor.*$",
    r"^.*Team$",
    r"^.*Editors$",
    r"^.*Staff$",
    r"^.*\bGroup\b.*$",
    r"^.*\bCompany\b.*$",
    r"^.*\bSolutions\b$",
    r"^.*\bCorporation\b.*$",
    r"^.*Strategy$",
    r"^[a-z0-9_.-]+@[a-z0-9.-]+",  # raw email
    r"^.*<[^>]+>.*",  # HTML
    r"^[a-zA-Z0-9_.-]+\.com$",  # domain-as-author
    r"^[A-Z][a-z]+ \w+ and [A-Z][a-z]+ [\w]+ and ",  # comma-blob authors with multiple "and"s
]
JUNK_AUTHOR_EXACT = {
    "info@digitalapplied.com (Digital Applied Team)",
    "netqyq@live.com (Calmops)",
    "Inflectra Corporation (webmaster@inflectra.com)",
    "official@x-cmd.com (X-CMD)",
    "contact@humanoidsdaily.com (Humanoids Daily Staff)",
    "arty.craftson@pottersquill.com (Arty Craftson)",
    "BeauHD",  # Slashdot editor robot — not a blogger
    "EditorDavid",  # Slashdot editor
    "msmash",  # Slashdot
    "Practical AI LLC",
    "GilPress",  # corporate brand alias
    "FutureCIO Editors",
    "Cribl",
    "BigPanda",
    "OpenClaw Team",
    "CyberArk Blog Team",
    "CISO Marketplace Team",
    "Sparkout Tech Solutions",
    "Metis Strategy",
    "IdeaPlan",
    "DataEndure",
    "LogRocket",
    "The Mad Botter",
    "The Chief I/O Team",
    "The Deep View",
    "Beyond the AI Hype",
    "Everyday AI",
    "Frey Design",
    "Forecasting Research Institute",
    "Bing Team",
    "AI Meets Girlboss",
    "Justin Brodley, Jonathan Baker, Ryan Lucas and Matt Kohn | Cloud Computing & AI News",
    "Andreas and Michael Wittig",  # actually two real people but presented as duo blog -> keep separately if you want, drop here for "individual" view
    "Wes Bos & Scott Tolinski - Full Stack JavaScript Web Developers",  # two real people, keep in podcaster bucket
    "Yaniv Bernstein and Chris Saad",
    "Jonas, Maximilian & Philip",
    "info@ddptechnologies.com (DDP Technologies)",
    "DataEndure",
}
JUNK_DOMAIN_EXACT = {
    "search.jobs.barclays",
    "nofluffjobs.com",
    "researchsquare.com",
    "lup.lub.lu.se",
    "vascularnews.com",
    "resources.rstudio.com",  # docs/help, not blog content
}


def is_junk_author(a: str) -> bool:
    if a in JUNK_AUTHOR_EXACT:
        return True
    for pat in JUNK_AUTHOR_PATTERNS:
        if re.fullmatch(pat, a, flags=re.IGNORECASE):
            return True
    if len(a) < 2 or len(a) > 80:
        return True
    if a.count(",") >= 2:  # multi-author blobs
        return True
    if "<" in a or ">" in a or "/>" in a:
        return True
    return False


def main() -> None:
    # Top 1000 authors by volume, with avg + sum authority and avg relevance
    body = {
        "indices": [INDEX],
        "query": {
            "size": 0,
            "query": {
                "bool": {
                    "filter": [
                        {"exists": {"field": "author"}},
                        {"exists": {"field": "authorAuthority"}},
                    ]
                }
            },
            "aggs": {
                "by_author": {
                    "terms": {"field": "author", "size": 1000, "min_doc_count": 5},
                    "aggs": {
                        "avg_auth": {"avg": {"field": "authorAuthority"}},
                        "sum_auth": {"sum": {"field": "authorAuthority"}},
                        "avg_rel": {"avg": {"field": "embeddingRelevance"}},
                        "domains": {"terms": {"field": "domain", "size": 3}},
                    },
                }
            },
        },
    }
    j = post(body)
    raw = j["aggregations"]["by_author"]["buckets"]
    print(f"Got {len(raw)} authors (min 5 posts)", file=sys.stderr)
    cleaned = []
    for b in raw:
        author = b["key"]
        if is_junk_author(author):
            continue
        domains = [x["key"] for x in b["domains"]["buckets"]]
        if all(d in JUNK_DOMAIN_EXACT for d in domains):
            continue
        cleaned.append(
            {
                "author": author,
                "n_posts": b["doc_count"],
                "avg_authority": b["avg_auth"]["value"],
                "sum_authority": b["sum_auth"]["value"],
                "avg_relevance": b["avg_rel"]["value"],
                "domains": domains,
            }
        )
    print(f"Cleaned: {len(cleaned)} candidate authors", file=sys.stderr)
    (OUT / "authors_cleaned.json").write_text(json.dumps(cleaned, indent=2))
    (OUT / "authors_raw.json").write_text(json.dumps(raw, indent=2))

    # Domains
    time.sleep(8)
    body = {
        "indices": [INDEX],
        "query": {
            "size": 0,
            "query": {"exists": {"field": "domainAuthority"}},
            "aggs": {
                "by_domain": {
                    "terms": {"field": "domain", "size": 1000, "min_doc_count": 5},
                    "aggs": {
                        "avg_da": {"avg": {"field": "domainAuthority"}},
                        "sum_da": {"sum": {"field": "domainAuthority"}},
                        "avg_rel": {"avg": {"field": "embeddingRelevance"}},
                    },
                }
            },
        },
    }
    j = post(body)
    raw_d = j["aggregations"]["by_domain"]["buckets"]
    cleaned_d = []
    for b in raw_d:
        if b["key"] in JUNK_DOMAIN_EXACT:
            continue
        cleaned_d.append(
            {
                "domain": b["key"],
                "n_posts": b["doc_count"],
                "avg_da": b["avg_da"]["value"],
                "sum_da": b["sum_da"]["value"],
                "avg_rel": b["avg_rel"]["value"],
            }
        )
    print(f"Got {len(raw_d)} domains, kept {len(cleaned_d)}", file=sys.stderr)
    (OUT / "domains_cleaned.json").write_text(json.dumps(cleaned_d, indent=2))


if __name__ == "__main__":
    main()
