"""Download US tech-role prose postings (with full text) via documentId-range pagination.
Global token gate at 44 req/min. Fails LOUDLY. Asserts recovery vs track_total_hits."""
import json, os, sys, time, threading
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = "https://api.skillenai.com/v1/query/search"
KEY = os.environ["API_KEY"]
BASEF = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
WORKERS, RPM = 3, 44.0
FIELDS = ["role","title","salaryMin","salaryMax","salaryCurrency","seniorityLevel",
          "companyCanonicalName","locationAdmin1","locationCity","platform","workModel",
          "sector","postedAt","postedAtSource","extractedText"]

_tl = threading.Lock(); _next=[0.0]
def gate():
    with _tl:
        now=time.monotonic(); t=max(now,_next[0]); _next[0]=t+60.0/RPM
    d=t-time.monotonic()
    if d>0: time.sleep(d)

def post(body, tries=8):
    data=json.dumps(body).encode(); last=None
    for i in range(tries):
        gate()
        req=urllib.request.Request(API,data=data,headers={"X-API-Key":KEY,"Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=300) as r: return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last=f"HTTP {e.code}: {e.read()[:300]!r}"
            if e.code in (429,500,502,503,504): time.sleep(min(60,5*(2**i))); continue
            raise RuntimeError(last)
        except Exception as e:
            last=f"{type(e).__name__}: {e}"; time.sleep(min(60,5*(2**i))); continue
    raise RuntimeError(f"exhausted retries; last error = {last}")

total = post({"query":{"size":0,"track_total_hits":True,"query":{"bool":{"filter":BASEF}}},
              "indices":["prod-enriched-jobs"]})["total"]
print("track_total_hits =", total, flush=True)

lock=threading.Lock(); out=open(OUT+".part","w"); n=[0]
def shard(c):
    hi = chr(ord(c)+1) if c!='f' else None
    cursor=None; got=0
    while True:
        rng={"gt":cursor} if cursor else {"gte":c}
        if hi: rng["lt"]=hi
        body={"query":{"size":100,"sort":[{"documentId":"asc"}],"_source":FIELDS,
               "query":{"bool":{"filter":BASEF+[{"range":{"documentId":rng}}]}}},
              "indices":["prod-enriched-jobs"]}
        hits=post(body).get("hits",[])
        if not hits: break
        with lock:
            for h in hits:
                h["_docid"]=h["_id"]; out.write(json.dumps(h)+"\n")
            out.flush(); n[0]+=len(hits)
            print(f"shard {c}: +{len(hits)} total {n[0]}", flush=True)
        cursor=hits[-1]["_id"]; got+=len(hits)
        if len(hits)<100: break
    print(f"SHARD {c} DONE {got}", flush=True)

with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    for f in [ex.submit(shard,c) for c in "0123456789abcdef"]: f.result()
out.close(); os.rename(OUT+".part", OUT)
ids=set()
for line in open(OUT): ids.add(json.loads(line)["_docid"])
print(f"wrote {n[0]} rows, {len(ids)} unique, target {total}", flush=True)
assert len(ids) >= 0.99*total, f"RECOVERY FAILURE {len(ids)} < 0.99*{total}"
print("RECOVERY OK", flush=True)
