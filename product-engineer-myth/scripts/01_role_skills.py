"""Aggregate top skills per role (PM / SWE / PE) using nested aggregations.

Outputs:
  role_doc_counts.json   — {role_label: total_postings_in_bucket}
  role_skills.json       — {role_label: [{skill, jobs_with_skill}, ...]}
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests

API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]
API_URL = os.environ.get("API_URL", "https://api.skillenai.com")

# Role buckets — use exact role.keyword matching, exclude management & specialized
ROLE_BUCKETS = {
    "Product Manager": [
        "Product Manager",
        "Senior Product Manager",
        "Staff Product Manager",
        "Principal Product Manager",
        "Lead Product Manager",
        "Group Product Manager",
        "Associate Product Manager",
        "Technical Product Manager",
        "AI Product Manager",
    ],
    "Software Engineer": [
        "Software Engineer",
        "Senior Software Engineer",
        "Staff Software Engineer",
        "Principal Software Engineer",
        "Lead Software Engineer",
        "Backend Software Engineer",
        "Frontend Software Engineer",
        "Full Stack Software Engineer",
        "Fullstack Software Engineer",
        "Full-Stack Software Engineer",
        "Software Development Engineer",
        "AI Software Engineer",
    ],
    "Product Engineer": [
        "Product Engineer",
        "AI Product Engineer",
        "Product Software Engineer",
        "Staff Product Engineer",
        "Lead Product Engineer",
        "Principal Product Engineer",
        "Full Stack Product Engineer",
        "Full-Stack Product Engineer",
        "Fullstack Product Engineer",
        "Fullstack Product Software Engineer",
        "Full Stack Product Software Engineer",
        "Backend Product Engineer",
        "Backend Product Software Engineer",
        "Frontend Product Engineer",
    ],
}

EXCLUDED_EMPLOYERS = ["Speechify"]


def role_query(roles: list[str]) -> dict:
    return {
        "bool": {
            "must": [{"terms": {"role.keyword": roles}}],
            "must_not": [
                {"term": {"companyCanonicalName.keyword": e}}
                for e in EXCLUDED_EMPLOYERS
            ],
        }
    }


def post(body: dict) -> dict:
    r = requests.post(
        f"{API_URL}/v1/query/search",
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json={"query": body, "indices": ["prod-enriched-jobs"]},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def fetch_role_skills(roles: list[str], top_k: int = 200) -> tuple[int, list[dict]]:
    """Returns (total_docs, skills_list) using nested aggregation on entities."""
    body = {
        "size": 0,
        "query": role_query(roles),
        "aggs": {
            "skill_entities": {
                "nested": {"path": "entities"},
                "aggs": {
                    "only_skills": {
                        "filter": {"term": {"entities.resolved.entityType": "skill"}},
                        "aggs": {
                            "by_skill": {
                                "terms": {
                                    "field": "entities.resolved.canonicalName.keyword",
                                    "size": top_k,
                                }
                            }
                        },
                    }
                },
            }
        },
    }
    res = post(body)
    total = res["total"]
    buckets = res["aggregations"]["skill_entities"]["only_skills"]["by_skill"][
        "buckets"
    ]
    skills = [
        {"skill": b["key"], "mentions": b["doc_count"]} for b in buckets
    ]
    return total, skills


def main() -> None:
    out_dir = Path(__file__).parent
    counts = {}
    skill_data = {}
    for role_label, roles in ROLE_BUCKETS.items():
        print(f"\n=== {role_label} ===")
        total, skills = fetch_role_skills(roles, top_k=200)
        print(f"  total docs: {total}")
        print(f"  unique top skills returned: {len(skills)}")
        for s in skills[:10]:
            print(f"    {s['mentions']:>6}  {s['skill']}")
        counts[role_label] = total
        skill_data[role_label] = skills
        time.sleep(2)

    (out_dir / "role_doc_counts.json").write_text(json.dumps(counts, indent=2))
    (out_dir / "role_skills.json").write_text(json.dumps(skill_data, indent=2))
    print("\nWrote role_doc_counts.json and role_skills.json")


if __name__ == "__main__":
    main()
