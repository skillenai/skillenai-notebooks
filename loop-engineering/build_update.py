#!/usr/bin/env python3
"""
Loop engineering — 2-week diffusion update (snapshot 2026-06-19, vs original 2026-06-11).
Pulls all "loop engineering"/"loop engineer" hits, classifies genuine vs collision with a
reproducible rule set, and renders the diffusion figures.
Run: API_KEY=... API_URL=... python3 build_update.py
"""
import json, os, csv, urllib.request, urllib.parse, re, collections
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

HERE = Path(__file__).parent
API_KEY = os.environ["API_KEY"]; API_URL = os.environ["API_URL"]
SNAP = "2026-06-19"  # this update
ORIG = "2026-06-11"  # original snapshot

def search(body):
    req = urllib.request.Request(API_URL+"/v1/query/search", data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=90))

q = {"bool":{"should":[
    {"match_phrase":{"extractedText":"loop engineering"}},
    {"match_phrase":{"extractedText":"loop engineer"}},
    {"match_phrase":{"title":"loop engineering"}}], "minimum_should_match":1}}
pat = re.compile(r".{0,70}loop[\s\W]{1,3}engineer.{0,60}", re.I)

# Reproducible classifier: high-precision collision rules; explicit boundary denylist; else genuine.
COLLISION_DENYLIST = {("techbytes.app","2026-05-15"), ("unifiedinfotech.net","2026-06-03")}
def classify(dom, date, snip, title):
    if (dom, date) in COLLISION_DENYLIST: return "collision"
    s = (snip + " " + title).lower()
    rules = ["hardware-in-the-loop","hardware in the loop","human-in-the-loop","human in the loop",
             "closed-loop","closed loop","feedback loop","feedback-loop","viral loop","protein",
             "inner-loop","inner loop","outer-loop","outer loop"]
    if any(r in s for r in rules): return "collision"
    if re.search(r"loop[:.]\s*engineer", s) and "loop engineering" not in s: return "collision"
    return "genuine"

rows = []
for idx in ["prod-enriched-blog","prod-enriched-news","prod-enriched-jobs","prod-enriched-scholarly","prod-enriched-social"]:
    d = search({"query":{"size":200,"track_total_hits":True,"query":q,
        "_source":["title","domain","publishedAt","extractedText","sourceUrl"]},"indices":[idx]})
    for h in d["hits"]:
        s = h.get("_source", h)
        txt = s.get("extractedText") or ""
        m = pat.search(txt); snip = m.group(0).replace("\n"," ").strip() if m else ""
        dom = (s.get("domain") or "") or urllib.parse.urlparse(s.get("sourceUrl") or "").netloc
        dom = dom.lower().replace("www.","")
        date = (s.get("publishedAt") or "")[:10]
        title = (s.get("title") or "").replace("\n"," ")
        if not date: continue
        rows.append({"date":date,"index":idx.replace("prod-enriched-",""),"domain":dom,
                     "title":title,"sense":classify(dom,date,snip,title),"snip":snip[:160]})
rows.sort(key=lambda r:r["date"])

gen = [r for r in rows if r["sense"]=="genuine"]
coll = [r for r in rows if r["sense"]=="collision"]
def win(rs, lo, hi): return [r for r in rs if lo <= r["date"] <= hi]
print(f"RAW total: {len(rows)} | genuine: {len(gen)} | collision: {len(coll)}")
print(f"genuine <=Jun10: {len(win(gen,'2000','2026-06-10'))} | Jun11-19: {len(win(gen,'2026-06-11','2026-06-99'))}")
print(f"collision <=Jun10: {len(win(coll,'2000','2026-06-10'))} | Jun11-19: {len(win(coll,'2026-06-11','2026-06-99'))}")

with open(HERE/"classified_hits_v2.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["date","index","domain","sense","title"])
    for r in rows: w.writerow([r["date"],r["index"],r["domain"],r["sense"],r["title"][:90]])

# ---------- Fig 04: diffusion timeline (daily genuine, Jun 1-19) ----------
dc = collections.Counter(r["date"] for r in gen if r["date"]>="2026-06-01")
days = [f"2026-06-{d:02d}" for d in range(1,20)]
dts = [datetime.strptime(d,"%Y-%m-%d") for d in days]
vals = [dc.get(d,0) for d in days]
fig, ax = plt.subplots(figsize=(12,4.8))
colors = ["#f0a89a" if d<="2026-06-10" else "#e8503a" for d in days]
ax.bar(dts, vals, width=0.7, color=colors, edgecolor="white", zorder=3)
for dt,v in zip(dts,vals):
    if v: ax.text(dt, v+0.12, str(v), ha="center", fontsize=9, fontweight="bold")
ax.axvline(datetime(2026,6,11), color="#888", ls=":", lw=1.2)
ax.text(datetime(2026,6,11), max(vals)+0.6, " original snapshot\n (saw 9 total)", fontsize=8.5, color="#555", va="top")
ax.annotate("Jun 7-8 ignition\n(Steinberger post → Osmani names it)", xy=(datetime(2026,6,8),1),
    xytext=(datetime(2026,6,2),6.5), fontsize=8.5, color="#222", arrowprops=dict(arrowstyle="->",color="#e8503a"))
ax.set_ylim(0,max(vals)+1.6); ax.set_ylabel("Genuine 'loop engineering'\narticles per day", fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d")); ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
ax.set_title("From blip to wave: 'loop engineering' kept diffusing for 9 straight days\n"
    f"Daily genuine articles, snapshot {SNAP} (lighter bars = pre-original-snapshot)", fontsize=12.5, fontweight="bold")
for sp in ["top","right"]: ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig(HERE/"04_diffusion_timeline.png", dpi=150, bbox_inches="tight"); plt.close()
print("Wrote 04_diffusion_timeline.png")

# ---------- Fig 05: the string-capture flip (genuine vs collision by window) ----------
windows = [("Baseline\n(pre Jun 8)","2000","2026-06-07"),
           ("Launch wave\n(Jun 8-10)","2026-06-08","2026-06-10"),
           ("Diffusion\n(Jun 11-19)","2026-06-11","2026-06-99")]
g = [len(win(gen,a,b)) for _,a,b in windows]
c = [len(win(coll,a,b)) for _,a,b in windows]
labels = [w[0] for w in windows]
fig, ax = plt.subplots(figsize=(9,5.2))
x = np.arange(len(windows))
ax.bar(x, c, color="#9aa7b4", label="Other meanings (HITL, HIL, inner-loop, …)")
ax.bar(x, g, bottom=c, color="#e8503a", label="Loop engineering (the buzzword)")
for i,(gi,ci) in enumerate(zip(g,c)):
    tot=gi+ci
    if tot: ax.text(i, tot+0.4, f"{gi}/{tot}\n{100*gi//tot}% genuine", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel('Documents matching "loop engineering"', fontsize=10)
ax.legend(fontsize=9.5, loc="upper left", frameon=False)
ax.set_title("The buzzword captured its own string\n"
    "Before Jun 8 the phrase mostly meant other things; by mid-June new matches are ~all the new sense",
    fontsize=12.5, fontweight="bold")
ax.set_ylim(0, max(gi+ci for gi,ci in zip(g,c))+6)
for sp in ["top","right"]: ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig(HERE/"05_string_capture.png", dpi=150, bbox_inches="tight"); plt.close()
print("Wrote 05_string_capture.png")

# ---------- breadth table data ----------
notable = [r for r in gen if r["date"]>="2026-06-11"]
print(f"\nGenuine Jun11-19 unique domains: {len(set(r['domain'] for r in notable))}")
print("Sample notable outlets:")
for dom in ["thenewstack.io","theregister.co.uk","hackernoon.com","pandaily.com","techsauce.co",
            "news.google.com","addyosmani.com","braingrid.ai","cioinsights.substack.com","blog.ripstech.com"]:
    hit = [r for r in rows if r["domain"]==dom]
    if hit: print(f"  {dom:26s} {hit[0]['date']} [{hit[0]['sense']}] {hit[0]['title'][:50]}")
