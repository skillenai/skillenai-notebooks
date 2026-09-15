"""Tech-role leaderboard race — Skillenai brand build.

Changes from v2:
  - Project/Program Manager and Business Analyst DROPPED. Both entered the corpus
    via the talent-graph ingest keyword list, not because they are tech roles:
    90% of "Program Manager" carries no technical qualifier and ~10% sit at
    defense primes; "Business Analyst" is led by McKinsey (their entry-level
    consultant title) and three health insurers. Removing them also removes them
    from the DENOMINATOR, so "share of tech hiring" is now actually tech.
  - Skillenai brand palette + Inter + logo stamp.
  - Tighter header; TOPN 15.

PALETTE NOTE: the brand ramp is one cyan->violet family and cannot carry 4
discrete identities (brand indigo vs violet = dE 2.0 deutan; deep blue vs violet
= dE 1.9). Validated set used here, all-pairs, surface #FBFCFE:
    #7A3FD1 violet | #22C1DA cyan | #E9A23B amber | #1BA36B green
    worst CVD dE 8.8 (protan), worst normal-vision dE 16.2 -> ALL CHECKS PASS.
Secondary encoding (always-visible colour-matched role labels + value labels)
is present, as required for the 8-9 CVD band.
"""
import json, collections, sys, math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
sys.path.insert(0,"/Users/jrand/git-repos/skillenai-notebooks/tech-role-pay-2026")
sys.path.insert(0,".")
import brand                                    # registers Inter + brand rcParams
from brand import BG, INK, GRID, MUTE, stamp
from allroles import GROUP

GC={"Software":"#22C1DA","Data":"#1BA36B","AI & ML":"#7A3FD1",
    "Infrastructure & Security":"#E9A23B","Product & Business":MUTE}
DROP={"Project / Program Manager","Business Analyst"}
rows=json.load(open("arrivals_all_roles.json"))
cnt=collections.Counter()
for r in rows:
    if r["r"] in DROP: continue
    cnt[(r["y"],r["m"],r["r"])]+=r["n"]
ROLES=sorted({r["r"] for r in rows}-DROP)
def win(y,m):
    a=collections.Counter()
    for _ in range(12):
        for rr in ROLES:
            v=cnt.get((y,m,rr),0)
            if v: a[rr]+=v
        m-=1
        if m==0: y,m=y-1,12
    return a
QS=[(y,m) for y in range(1996,2026) for m in (3,6,9,12)]
QS=[q for q in QS if q<=(2025,9)]
LAST_SOLID=(2025,6)
SHARE={}
for q in QS:
    a=win(*q); t=sum(a.values()) or 1
    SHARE[q]={r:100*a[r]/t for r in ROLES}
RK={q:{r:i for i,r in enumerate(sorted(ROLES,key=lambda x:-SHARE[q][x]))} for q in QS}
TOPN=15; FLOOR=0.02; SUB=18
def smooth(x): return x*x*(3-2*x)
FRAMES=[(0,0.0)]*20
for i in range(len(QS)-1):
    for k in range(SUB): FRAMES.append((i,k/SUB))
FRAMES += [(len(QS)-2,1.0)]*75
MN={3:"Q1",6:"Q2",9:"Q3",12:"Q4"}
XMIN,XMAX=0.07,46.0
fig,ax=plt.subplots(figsize=(12.2,7.0))
fig.subplots_adjust(top=.855,bottom=.135,left=.225,right=.962)   # tighter header
fig.text(.022,.975,"30 years of tech hiring, ranked",fontsize=18.5,weight="bold",color=INK,va="top",ha="left")
fig.text(.022,.928,"Share of all tech role arrivals, trailing 12 months. Log scale.",
         fontsize=10.2,color=MUTE,va="top",ha="left")
date_txt=fig.text(.962,.972,"",fontsize=27,weight="bold",color=INK,ha="right",va="top")
prov=fig.text(.962,.912,"",fontsize=8.6,color="#D64545",ha="right",va="top",style="italic")
def draw(fr):
    i,f=fr; q0,q1=QS[i],QS[i+1]; e=smooth(f)
    ax.clear()
    ax.set_xscale("log"); ax.set_xlim(XMIN,XMAX); ax.set_ylim(TOPN-0.3,-1.0)
    for s in ("left","right","top"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_yticks([]); ax.grid(axis="x",color=GRID,alpha=.75,lw=.7); ax.set_axisbelow(True)
    ax.set_xticks([.1,.5,1,2,5,10,20,40])
    ax.set_xticklabels(["0.1%","0.5%","1%","2%","5%","10%","20%","40%"],fontsize=9)
    ax.tick_params(length=0)
    ax.set_xlabel("Share of tech role arrivals (trailing 12 months, log scale)",fontsize=9.6,color=MUTE)
    for r in ROLES:
        v0,v1=max(SHARE[q0][r],FLOOR),max(SHARE[q1][r],FLOOR)
        v=math.exp(math.log(v0)+(math.log(v1)-math.log(v0))*e)
        y=RK[q0][r]+(RK[q1][r]-RK[q0][r])*e
        # keep the fade band INSIDE the axes so entering rows never overlap the ticks
        if y>TOPN-0.45: continue
        a=1.0 if y<=TOPN-1.45 else max(0.0,(TOPN-0.45-y))
        if a<=.02: continue
        col=GC[GROUP.get(r,"Product & Business")]
        ax.barh(y,v,height=.68,color=col,alpha=a)
        ax.text(-0.012,y,r,ha="right",va="center",fontsize=10.2,weight="semibold",
                color=col,alpha=a,clip_on=False,transform=ax.get_yaxis_transform())
        ax.text(v*1.06,y,f"{v:.1f}%",va="center",fontsize=9.4,weight="bold",color=INK,alpha=a)
    cur=q0 if e<.5 else q1
    date_txt.set_text(f"{MN[cur[1]]} {cur[0]}")
    prov.set_text("provisional - reporting lag" if cur>LAST_SOLID else "")
    return []
h=[plt.Rectangle((0,0),1,1,color=GC[g]) for g in GC]
fig.legend(h,list(GC),loc="lower center",ncol=5,frameon=False,fontsize=9.6,bbox_to_anchor=(.50,.002))
stamp(fig,x=.878,y=.012,h=.040)                                  # Skillenai logo, bottom-right
ani=FuncAnimation(fig,draw,frames=FRAMES,blit=False)
ani.save("07_role_race.mp4",writer=FFMpegWriter(fps=30,bitrate=3400,
         extra_args=["-pix_fmt","yuv420p"]),dpi=100)
print(f"wrote 07_role_race.mp4  {len(FRAMES)}f @30fps = {len(FRAMES)/30:.0f}s  "
      f"{os.path.getsize('07_role_race.mp4')/1048576:.1f} MB")
a=win(2025,6); t=sum(a.values())
print(f"final board (n={t:,}): "+", ".join(f"{k} {100*v/t:.1f}%" for k,v in a.most_common(6)))
