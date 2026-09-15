"""Pass 3: every tech-role arrival across both snapshots, month precision.
Arrival = spell start whose preceding spell was a DIFFERENT role (consecutive
same-role runs collapsed, so a company change inside a role is not an arrival)."""
import json,os,re,sys,collections
sys.path.insert(0,'.')
from allroles import role_of
DATA="/Users/jrand/git-repos/skillenai-ds/work/company-eliteness/talent_graph/_data"
MON={m:i+1 for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])}
def pd_(s):
    if not s: return None
    s=str(s).strip()
    m=re.fullmatch(r'([A-Z][a-z]{2})\w*\s+(\d{4})',s)
    if m: return (int(m.group(2)),MON[m.group(1)])
    m=re.fullmatch(r'(\d{4})-(\d{2})',s)
    if m: return (int(m.group(1)),int(m.group(2)))
    return None
seen=set(); arr=collections.Counter(); n=0
for fn in ["profiles.jsonl","bd_20260824_144100.jsonl"]:
    for line in open(os.path.join(DATA,fn),encoding='utf-8',errors='replace'):
        try: p=json.loads(line)
        except: continue
        lid=p.get('linkedin_id') or p.get('id')
        if not lid or lid in seen: continue
        seen.add(lid); n+=1
        S=[]
        for e in (p.get('experience') or []):
            for r in (e.get('positions') or [e]):
                if not isinstance(r,dict): continue
                t=r.get('title'); d=pd_(r.get('start_date'))
                if t and d: S.append((d,t))
        S.sort(key=lambda x:(x[0][0],x[0][1]))
        prev=None
        for (d,t) in S:
            rr=role_of(t)
            if rr and rr!=prev and 1990<=d[0]<=2025:
                arr[(d[0],d[1],rr)]+=1
            prev=rr
        if n%150000==0: print(f"  ...{n} profiles",flush=True)
json.dump([{"y":y,"m":m,"r":r,"n":c} for (y,m,r),c in sorted(arr.items())],
          open("arrivals_all_roles.json","w"))
print("profiles",n,"| distinct (year,month,role) cells",len(arr),"| total arrivals",sum(arr.values()))
