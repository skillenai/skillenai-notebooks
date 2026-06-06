"""For each under-covered skill, find the top blog authors writing about it.

Then aggregate cross-skill: which authors are multi-skill gap-fillers?
"""
import csv
import json
import os
import pathlib
import re
import time
from collections import defaultdict

import requests

API_URL = "https://api.skillenai.com"
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

# Top under-covered skills (from /tmp/ranked_skills.json) — pick the 12 most under-covered.
GAP_SKILLS = {
    "Looker": ["Looker"],
    "Tableau": ["Tableau"],
    "Power BI": ["Power BI"],
    "Kotlin": ["Kotlin"],
    "Scala": ["Scala"],
    "Spring Boot": ["Spring Boot"],
    "GCP": ["GCP", "Google Cloud Platform"],
    "Airflow": ["Apache Airflow", "Airflow"],
    "Terraform": ["Terraform"],
    "Jenkins": ["Jenkins"],
    "DBT": ["dbt"],
    "Ansible": ["Ansible"],
}

# Junk-author filter (memory: feedback on /tmp/influential-tech-bloggers/fetch_rankings.py)
JUNK_GENERIC = {"", "admin", "Admin", "Author", "author", "Unknown", "unknown", "user", "Editor", "editor"}
JUNK_REGEXES = [
    re.compile(r"^.+@.+\..+$"),                # email
    re.compile(r"<[^>]+>"),                    # html tags
    re.compile(r"https?://"),                  # URL in name
    re.compile(r"gravatar\.com"),              # gravatar
    re.compile(r"\.(com|net|org|io|ai|cloud|website|page|top)$", re.I),  # domain-as-author
]
JUNK_SUFFIXES = ("Team", "team", "Editors", "Staff", "Bot", "News")
JUNK_BOTS = {"BeauHD", "EditorDavid", "msmash", "Soulskill", "Slashdot", "feedfetcher"}

def is_junk(a: str) -> bool:
    if not a or a in JUNK_GENERIC or a in JUNK_BOTS:
        return True
    if a.count(",") >= 2:  # multi-author blob
        return True
    if any(a.endswith(s) for s in JUNK_SUFFIXES):
        return True
    for rgx in JUNK_REGEXES:
        if rgx.search(a):
            return True
    if len(a) > 80 or len(a) < 2:
        return True
    return False

# Load PBN denylist
pbn_path = pathlib.Path("/Users/jrand/git-repos/skillenai-notebooks/synthetic-breakout-may-2026/network_domains_seed.csv")
pbn_domains: list[str] = []
if pbn_path.exists():
    rdr = csv.reader(pbn_path.open())
    next(rdr)
    pbn_domains = [row[0].strip() for row in rdr if row and row[0].strip()]

SKI274 = ["search.jobs.barclays.com", "nofluffjobs.com", "vascularnews.com", "researchsquare.com", "lup.lub.lu.se"]

def phrase_clause(phrases):
    if len(phrases) == 1:
        return {"match_phrase": {"extractedText": phrases[0]}}
    return {"bool": {"should": [{"match_phrase": {"extractedText": p}} for p in phrases], "minimum_should_match": 1}}

def query(body):
    r = requests.post(f"{API_URL}/v1/query/search",
                      headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
                      json=body, timeout=60)
    if r.status_code == 429:
        time.sleep(12); return query(body)
    r.raise_for_status()
    return r.json()

# For each skill, aggregate by author (top 100), then post-filter junk.
per_skill_authors: dict[str, list[tuple[str, int, float]]] = {}  # author -> (name, count, avg_authority)
all_author_appearances = defaultdict(lambda: {"skills": [], "total_posts": 0, "max_authority": 0.0, "domain_top": ""})

for skill, phrases in GAP_SKILLS.items():
    print(f"\n--- {skill} ---")
    body = {
        "indices": ["prod-enriched-blog"],
        "query": {
            "size": 0,
            "track_total_hits": True,
            "query": {
                "bool": {
                    "must": [phrase_clause(phrases), {"exists": {"field": "author"}}],
                    "must_not": [{"terms": {"domain": pbn_domains + SKI274}}],
                }
            },
            "aggs": {
                "authors": {
                    "terms": {"field": "author", "size": 100},
                    "aggs": {
                        "avg_auth": {"avg": {"field": "authorAuthority"}},
                        "top_domain": {"terms": {"field": "domain", "size": 1}},
                    }
                }
            }
        }
    }
    d = query(body)
    total = d.get("total", 0)
    buckets = d["aggregations"]["authors"]["buckets"]
    cleaned = []
    for b in buckets:
        name = b["key"]
        if is_junk(name):
            continue
        cnt = b["doc_count"]
        if cnt < 2:
            continue
        avg_auth = b["avg_auth"]["value"] or 0.0
        top_dom_buckets = b["top_domain"]["buckets"]
        top_dom = top_dom_buckets[0]["key"] if top_dom_buckets else ""
        cleaned.append((name, cnt, avg_auth, top_dom))
        all_author_appearances[name]["skills"].append((skill, cnt, avg_auth))
        all_author_appearances[name]["total_posts"] += cnt
        all_author_appearances[name]["max_authority"] = max(all_author_appearances[name]["max_authority"], avg_auth)
        all_author_appearances[name]["domain_top"] = top_dom
    cleaned.sort(key=lambda r: -r[1])
    per_skill_authors[skill] = cleaned[:20]
    print(f"  total posts ({skill}): {total:,}; cleaned author rows: {len(cleaned)}")
    for name, cnt, auth, dom in cleaned[:10]:
        print(f"   {cnt:>4} posts  auth={auth:5.2f}  {name:35} @ {dom}")
    time.sleep(2.0)

# Multi-skill gap-fillers
print("\n\n=== MULTI-SKILL GAP-FILLERS (authors writing across multiple under-covered skills) ===")
multi = []
for name, v in all_author_appearances.items():
    skills_covered = [s for s, c, a in v["skills"] if c >= 2]
    if len(skills_covered) >= 2:
        multi.append((name, len(set(s for s, c, a in v["skills"])), v["total_posts"], v["max_authority"], v["domain_top"], v["skills"]))
multi.sort(key=lambda r: (-r[1], -r[2]))
for name, n_skills, total_posts, max_auth, dom, skills in multi[:30]:
    sk = ", ".join(f"{s}({c})" for s, c, a in sorted(skills, key=lambda x: -x[1])[:6])
    print(f"  {n_skills} skills · {total_posts:>3} posts · max_auth {max_auth:.2f} · {name:30} @ {dom}")
    print(f"       skills: {sk}")

# Save
out = {
    "per_skill_authors": {s: [{"author": n, "posts": c, "avg_authority": a, "top_domain": d} for n, c, a, d in lst]
                          for s, lst in per_skill_authors.items()},
    "multi_skill_gap_fillers": [
        {"author": n, "n_skills": ns, "total_posts": tp, "max_authority": ma, "top_domain": dom,
         "skills": [{"skill": s, "posts": c, "avg_authority": a} for s, c, a in sk]}
        for n, ns, tp, ma, dom, sk in multi[:50]
    ],
}
pathlib.Path("/tmp/gap_authors.json").write_text(json.dumps(out, indent=2))
print(f"\nWrote /tmp/gap_authors.json")
