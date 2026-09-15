"""Group-share history: the structural story the role-level race cannot show.
Infrastructure never grew as a share - its INSIDES were replaced."""
import json, collections, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0,'.')
sys.path.insert(0,'/Users/jrand/git-repos/skillenai-notebooks/tech-role-pay-2026')
import brand
from brand import BG,INK,GRID,MUTE,stamp
INK2=MUTE; SURF=BG
def save(fig,p):
    fig.savefig(p,dpi=150,bbox_inches='tight',facecolor=BG); plt.close(fig); print('wrote',p)
from allroles import GROUP
DROP={"Project / Program Manager","Business Analyst"}   # not tech roles; see race3.py
rows=json.load(open("arrivals_all_roles.json"))
cnt=collections.Counter()
for r in rows: cnt[(r["y"],r["m"],r["r"])]+=r["n"]
ROLES=sorted({r["r"] for r in rows}-DROP)
YRS=list(range(1996,2026))
def yshare(y):
    a=collections.Counter()
    for rr in ROLES:
        for m in range(1,13): a[rr]+=cnt.get((y,m,rr),0)
    t=sum(a.values()) or 1
    return a,t
GC={"Software":"#22C1DA","Data":"#1BA36B","AI & ML":"#7A3FD1",
    "Infrastructure & Security":"#E9A23B","Product & Business":MUTE}
ORDER=["Software","Product & Business","Infrastructure & Security","Data","AI & ML"]
series={g:[] for g in ORDER}; totals=[]
for y in YRS:
    a,t=yshare(y); totals.append(t)
    for g in ORDER: series[g].append(100*sum(v for k,v in a.items() if GROUP.get(k)==g)/t)
fig,(ax,ax2)=plt.subplots(1,2,figsize=(15,5.8),gridspec_kw={"width_ratios":[1.25,1]})
ax.stackplot(YRS,[series[g] for g in ORDER],colors=[GC[g] for g in ORDER],
             labels=ORDER,edgecolor=SURF,linewidth=.7)
ax.set_xlim(1996,2025); ax.set_ylim(0,100); ax.set_ylabel("Share of tech role arrivals (%)")
# label each band at ITS OWN midpoint in the final year (never hardcode - the
# band heights change whenever the role set or denominator changes)
cum=0.0
for g in ORDER:
    v=series[g][-1]; mid=cum+v/2; cum+=v
    if v>=4.5:
        ax.text(2024.4,mid,g,ha="right",va="center",fontsize=9.6,weight="bold",color="white")
ax.set_title("Software went from 69% of tech hiring to 41%",fontsize=13.5,fontweight="bold",loc="left",pad=10)
# right panel: inside Infrastructure
INF=["Infrastructure Engineer","Network Engineer","DevOps Engineer","Security Engineer",
     "Site Reliability Engineer","Platform Engineer","Cloud Engineer"]
IC=["#E9A23B","#B4762A","#22C1DA","#1BA36B","#7A3FD1","#D64545",MUTE]
ends=[]
for r,c in zip(INF,IC):
    v=[100*yshare(y)[0][r]/yshare(y)[1] for y in YRS]
    ax2.plot(YRS,v,color=c,lw=2); ends.append([v[-1],r,c])
ends.sort(key=lambda x:-x[0])          # de-collide end labels with a min gap
gap=0.30
for i in range(1,len(ends)):
    if ends[i-1][0]-ends[i][0]<gap: ends[i][0]=ends[i-1][0]-gap
for yv,r,c in ends:
    ax2.annotate(r,(YRS[-1],yv),xytext=(7,0),textcoords="offset points",
                 fontsize=8.6,color=c,va="center",fontweight="bold")
ax2.set_xlim(1996,2031); ax2.set_ylim(-0.5,6.2); ax2.set_ylabel("Share of tech role arrivals (%)")
ax2.set_title("Inside infrastructure: total churn, no growth",fontsize=13.5,fontweight="bold",loc="left",pad=10)
ax2.grid(axis="y",color=GRID,lw=.8); ax2.set_axisbelow(True)
for a in (ax,ax2):
    a.tick_params(labelsize=9.5)
    for s in ("top","right"): a.spines[s].set_visible(False)
fig.suptitle("Thirty years of tech hiring, by role group",fontsize=17,fontweight="bold",x=.045,ha="left",y=.99)
fig.text(.045,.915,"Share of all classified tech role arrivals per calendar year, Skillenai talent graph. Infrastructure & Security held a 9-12% band throughout \u2014 "
        "sysadmins and network engineers were replaced by DevOps, cloud and security. Excludes Program Manager and Business Analyst (see methodology).",
        color=INK2,fontsize=9.8)
fig.tight_layout(rect=[0,.055,1,.885])
stamp(fig,x=.885,y=.004,h=.038)
save(fig,"08_group_shares.png")
print("group shares 1998 vs 2025:")
for g in ORDER: print(f"   {g:<28}{series[g][YRS.index(1998)]:>6.1f}% -> {series[g][YRS.index(2025)]:>6.1f}%")
