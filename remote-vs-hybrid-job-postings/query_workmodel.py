#!/usr/bin/env python3
"""
Pull work-model (remote / hybrid / onsite) distributions from the Skillenai
job-posting index, broken down overall and by seniority, country, and role.

Output: workmodel_results.json (raw aggregation counts — the evidence record).

Usage:
    export API_KEY=...            # Skillenai insights API key
    export API_URL=https://api.skillenai.com
    python3 query_workmodel.py

Data quality filters applied:
  - Speechify excluded (companyCanonicalName.keyword) — single employer that
    carpet-bombs ~5k identical 100%-remote postings across cities.
  - workModel is a clean keyword field (~99.9% coverage). 'remote' and 'hybrid'
    are positively text-detected; 'onsite' is the residual bucket.
"""
import json
import os
import urllib.request

API_KEY = os.environ["API_KEY"]
API_URL = os.environ.get("API_URL", "https://api.skillenai.com")

NO_SPAM = {"bool": {"must_not": [{"terms": {"companyCanonicalName.keyword": ["Speechify"]}}]}}
WM = {"terms": {"field": "workModel", "size": 4}}

BODY = {
    "query": {
        "size": 0,
        "query": NO_SPAM,
        "aggs": {
            "wm": WM,
            "by_sen": {"terms": {"field": "seniorityLevel", "size": 12}, "aggs": {"wm": WM}},
            "by_country": {"terms": {"field": "locationCountry", "size": 12}, "aggs": {"wm": WM}},
            "by_role": {"terms": {"field": "role.keyword", "size": 18}, "aggs": {"wm": WM}},
        },
    },
    "indices": ["prod-enriched-jobs"],
}


def main():
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps(BODY).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        d = json.load(resp)
    aggs = d["aggregations"]
    with open("workmodel_results.json", "w") as f:
        json.dump(aggs, f, indent=2)
    print("wrote workmodel_results.json")


if __name__ == "__main__":
    main()
