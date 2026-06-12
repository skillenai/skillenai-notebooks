#!/usr/bin/env python3
"""
Loop engineering: anatomy of a buzzword caught at birth.
Fetches blog lineage trajectories (prompt -> context -> loop), applies the
PBN content-farm domain denylist to the denominator, and renders 3 figures.
Run: API_KEY=... API_URL=... python3 build_analysis.py
"""
import json, os, csv, urllib.request, collections
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

HERE = Path(__file__).parent
API_KEY = os.environ["API_KEY"]; API_URL = os.environ["API_URL"]
PBN_CSV = "/Users/jrand/git-repos/skillenai-notebooks/synthetic-breakout-may-2026/network_domains_seed.csv"

def search(body):
    req = urllib.request.Request(API_URL + "/v1/query/search", data=json.dumps(body).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))

pbn = []
with open(PBN_CSV) as f:
    r = csv.reader(f); next(r, None)
    for row in r:
        if row: pbn.append(row[0].strip().lower())

# ---- The 27 raw match_phrase hits, hand-classified by snippet sense ----
# sense GENUINE = the agentic "loop engineering" coinage; everything else is a string collision
HITS = [
 ("2026-05-07","blog","podrocket.logrocket.com","GENUINE","agentic loop engineering with auto research"),
 ("2026-05-11","blog","anup.io","GENUINE","Welcome to Middle Loop Engineering"),
 ("2026-06-08","news","alphasignalai.substack.com","GENUINE","Loop engineering is building a system that prompts your agent"),
 ("2026-06-09","blog","sumantthakur.substack.com","GENUINE","Loop engineering is replacing prompt engineering"),
 ("2026-06-09","news","antoinebuteau.com","GENUINE","Loop Engineering. - Addy Osmani"),
 ("2026-06-09","news","bensbites.substack.com","GENUINE","Loop Engineering by Addy Osmani"),
 ("2026-06-09","news","mer.vin","GENUINE","Loop engineering means you stop being the person who types"),
 ("2026-06-10","blog","blog.scrapinghub.com","GENUINE","Addy Osmani has given the practice a name: loop engineering"),
 ("2026-06-10","news","linas.substack.com","GENUINE","from manual prompter to loop engineer"),
 # collisions
 ("2026-03-30","jobs","jobs.ashbyhq.com","PROTEIN","loop engineering, protein-protein complex structure"),
 ("2026-05-18","jobs","job-boards.greenhouse.io","CLOSED-LOOP","closed-loop engineering system"),
 ("2026-03-29","jobs","jobs.lever.co","HIL","Hardware-in-the-Loop Engineer"),
 ("2026-04-30","jobs","careers.jhuapl.edu","HIL","Senior Embedded Systems & Hardware-in-the-Loop Engineer"),
 ("2026-04-30","jobs","careers.jhuapl.edu","HIL","Hardware in the Loop Engineer"),
 ("2026-04-14","blog","preprod.cloud","HIL","hardware-in-the-loop engineering (PBN)"),
 ("2026-03-30","jobs","boards.greenhouse.io","INTERVIEW-LOOP","Loop: Engineering Leadership Interview"),
 ("2026-03-30","jobs","boards.greenhouse.io","INTERVIEW-LOOP","Loop: Engineering Leadership Interview"),
 ("2026-05-02","jobs","jobs.generalcatalyst.com","INTERVIEW-LOOP","Loop: Engineering Leadership Interview"),
 ("2026-04-24","blog","softwareseni.com","HITL","Human-in-the-Loop (engineer drives and approves)"),
 ("2026-05-09","blog","qbitshared.com","HITL","human-in-the-loop engineering workflows"),
 ("2026-05-21","blog","embarkingonvoyage.com","HITL","Human-in-the-Loop Engineering"),
 ("2026-05-23","scholarly","cs.ai","HITL","human-in-the-loop engineering, limiting transferability"),
 ("2026-01-04","blog","mwolson.org","SENTENCE-BOUNDARY","autonomous loop: Engineer picks up a task"),
 ("2026-03-11","blog","powerapp.pro","SENTENCE-BOUNDARY","closes the loop: engineering delivers (PBN)"),
 ("2026-05-15","blog","techbytes.app","SENTENCE-BOUNDARY","evaluation loop, engineering teams"),
 ("2026-04-11","blog","kickstarts.info","FEEDBACK-LOOP","feedback-loop engineering (PBN)"),
 ("2026-05-27","blog","martech360.com","VIRAL-LOOP","Viral Loop Engineering (growth marketing)"),
]
with open(HERE/"classified_hits.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["date","index","domain","sense","snippet"])
    w.writerows(HITS)
print(f"Wrote classified_hits.csv ({len(HITS)} rows)")

# ================= Figure 1: the disambiguation =================
sense_counts = collections.Counter(h[3] for h in HITS)
order = ["GENUINE","HITL","HIL","INTERVIEW-LOOP","SENTENCE-BOUNDARY","CLOSED-LOOP","FEEDBACK-LOOP","PROTEIN","VIRAL-LOOP"]
labels = {"GENUINE":"Loop engineering\n(the new buzzword)","HITL":"Human-in-the-loop","HIL":"Hardware-in-the-loop",
 "INTERVIEW-LOOP":'Interview "loop"',"SENTENCE-BOUNDARY":"Sentence-boundary\nnoise","CLOSED-LOOP":"Closed-loop control",
 "FEEDBACK-LOOP":"Feedback loop","PROTEIN":"Protein loop\n(comp. biology)","VIRAL-LOOP":"Viral loop\n(marketing)"}
vals=[sense_counts[s] for s in order]
cols=["#e8503a"]+["#9aa7b4"]*(len(order)-1)
fig,ax=plt.subplots(figsize=(10,5.5))
y=np.arange(len(order))[::-1]
ax.barh(y,vals,color=cols,edgecolor="white")
for yi,v in zip(y,vals): ax.text(v+0.15,yi,str(v),va="center",fontsize=11,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([labels[s] for s in order],fontsize=10)
ax.set_xlabel('Documents matching the string "loop engineering" / "loop engineer"',fontsize=10)
ax.set_title('The string "loop engineering" collides with eight other things\n'
 f'Only {sense_counts["GENUINE"]} of {len(HITS)} raw matches are the new agentic buzzword',fontsize=12.5,fontweight="bold")
ax.set_xlim(0,max(vals)+1.2)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(HERE/"01_disambiguation.png",dpi=150,bbox_inches="tight"); plt.close()
print("Wrote 01_disambiguation.png")

# ================= Figure 2: the birth timeline =================
gen=[h for h in HITS if h[3]=="GENUINE"]
daycount=collections.Counter(h[0] for h in gen)
days=sorted(daycount)
dts=[datetime.strptime(d,"%Y-%m-%d") for d in days]
fig,ax=plt.subplots(figsize=(11,4.8))
ax.bar(dts,[daycount[d] for d in days],width=2.2,color="#e8503a",edgecolor="white",zorder=3)
for d,dt in zip(days,dts):
    ax.text(dt,daycount[d]+0.08,str(daycount[d]),ha="center",fontsize=10,fontweight="bold")
ax.set_ylim(0,max(daycount.values())+1.4)
ax.set_ylabel("Genuine 'loop engineering'\narticles per day",fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
ax.annotate("May 7-11: proto-uses\n('agentic loop eng.', 'middle loop eng.')",
    xy=(datetime(2026,5,9),1.05),xytext=(datetime(2026,5,9),3.1),fontsize=8.5,ha="center",color="#555",
    arrowprops=dict(arrowstyle="-",color="#bbb"))
ax.annotate("Jun 7: Peter Steinberger's one-liner\nsparks the hype on X; Addy Osmani\nnames it 'loop engineering'",
    xy=(datetime(2026,6,9),daycount.get("2026-06-09",4)),xytext=(datetime(2026,5,18),3.5),fontsize=8.5,ha="left",color="#222",
    arrowprops=dict(arrowstyle="->",color="#e8503a"))
ax.set_title("A buzzword caught at birth: 'loop engineering' in the Skillenai corpus\n"
 "7 articles in 3 days (Jun 8-10, 2026); corpus snapshot taken Jun 11",fontsize=12.5,fontweight="bold")
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(HERE/"02_birth_timeline.png",dpi=150,bbox_inches="tight"); plt.close()
print("Wrote 02_birth_timeline.png")

# ================= Figure 3: the lineage (blog, PBN-denylisted denominator) =================
TERMS={"prompt engineering":"prompt engineering","context engineering":"context engineering",
       "agentic loop":"agentic loop","loop engineering":"loop engineering"}
filt={k:{"match_phrase":{"extractedText":v}} for k,v in TERMS.items()}
body={"query":{"size":0,"query":{"bool":{"filter":[{"range":{"publishedAt":{"gte":"2024-06-01","lte":"2026-06-11"}}}],
        "must_not":[{"terms":{"domain":pbn}}]}},
    "aggs":{"by":{"date_histogram":{"field":"publishedAt","calendar_interval":"month","min_doc_count":0},
        "aggs":{"f":{"filters":{"filters":filt}}}}}},"indices":["prod-enriched-blog"]}
d=search(body)
buckets=d["aggregations"]["by"]["buckets"]
rows=[]
for m in buckets:
    tot=m["doc_count"]
    if tot==0: continue
    mon=m["key_as_string"][:7]
    if mon>"2026-06": continue
    f=m["f"]["buckets"]
    rows.append((mon,tot,{k:f[k]["doc_count"] for k in TERMS}))
with open(HERE/"lineage_blog_share.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["month","blog_docs_excl_pbn"]+["%s_per10k"%k.replace(" ","_") for k in TERMS])
    for mon,tot,c in rows:
        w.writerow([mon,tot]+[round(c[k]/tot*10000,2) for k in TERMS])
months=[datetime.strptime(r[0]+"-01","%Y-%m-%d") for r in rows]
fig,ax=plt.subplots(figsize=(11,5.8))
styles={"prompt engineering":("#1f4e79","-"),"context engineering":("#2e8b57","-"),
        "agentic loop":("#d98c00","--"),"loop engineering":("#e8503a","-")}
for k in TERMS:
    yk=[r[2][k]/r[1]*10000 for r in rows]
    c,ls=styles[k]
    ax.plot(months,yk,ls,color=c,lw=2.6 if k in ("prompt engineering","loop engineering") else 2.0,
            marker="o",ms=3.5,label=k)
ax.set_ylabel("Mentions per 10,000 blog posts\n(content-farm / PBN domains excluded)",fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.legend(fontsize=10,loc="upper left",frameon=False)
ax.set_title("The lineage: prompt -> context -> loop engineering\n"
 "Blog mentions per 10k posts, Jun 2024 - Jun 2026",fontsize=12.5,fontweight="bold")
ax.annotate("'loop engineering' barely\nregisters - it's days old",
    xy=(months[-1],rows[-1][2]["loop engineering"]/rows[-1][1]*10000),
    xytext=(datetime(2025,8,1),60),fontsize=9,color="#e8503a",
    arrowprops=dict(arrowstyle="->",color="#e8503a"))
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(HERE/"03_lineage.png",dpi=150,bbox_inches="tight"); plt.close()
print("Wrote 03_lineage.png")
print("\nLineage tail (per 10k, PBN-excluded):")
for mon,tot,c in rows[-8:]:
    print(f"  {mon} n={tot:6d} " + " ".join(f"{k.split()[0]}={c[k]/tot*10000:6.1f}" for k in TERMS))
