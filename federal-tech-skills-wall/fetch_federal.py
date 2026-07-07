"""Download the current federal (sector=public) subset from the Skillenai job index -> federal_now.json.
Requires SKILLENAI_INSIGHTS_API_KEY in the environment."""
import json, time, urllib.request, os
KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]; URL = "https://api.skillenai.com"
def q(b):
    r = urllib.request.Request(URL + "/v1/query/search", data=json.dumps(b).encode(),
        headers={"X-API-Key": KEY, "Content-Type": "application/json"})
    for a in range(6):
        try: return json.load(urllib.request.urlopen(r, timeout=120))
        except Exception: time.sleep(2 ** a)
    raise SystemExit("fail")
src = ["title","role","seniorityLevel","workModel","salaryMin","salaryMax","salaryCurrency","postedAt","extractedText","entities"]
out, frm = [], 0
while True:
    d = q({"indices": ["prod-enriched-jobs"], "query": {"size": 100, "from": frm,
        "query": {"term": {"sector": "public"}}, "_source": src}})
    h = d["hits"]
    if not h: break
    out += h; frm += 100
    if len(h) < 100: break
    time.sleep(1.5)
json.dump(out, open("federal_now.json", "w")); print("downloaded", len(out))
