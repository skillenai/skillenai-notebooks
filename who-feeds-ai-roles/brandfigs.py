"""Report figures on the Skillenai brand system, six roles.
Palette per race3.py (validated all-pairs, surface #FBFCFE)."""
import json,collections,sys,math,random
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0,"/Users/jrand/git-repos/skillenai-notebooks/tech-role-pay-2026"); sys.path.insert(0,".")
import brand
from brand import BG,INK,GRID,MUTE,stamp
CY,GR,VI,AM,RD="#22C1DA","#1BA36B","#7A3FD1","#E9A23B","#D64545"
ORDER=["AI Researcher","Data Scientist","ML Engineer","AI Engineer","Data Analyst","Data Engineer"]
RC={"AI Researcher":VI,"ML Engineer":VI,"AI Engineer":VI,
    "Data Scientist":GR,"Data Analyst":GR,"Data Engineer":GR}
E=json.load(open("phd_extended.json")); F=json.load(open("final.json"))
FD=json.load(open("flows_data_roles.json"))
phd,adeg,N=E['phd'],E['adeg'],E['N']
base=100*F['phd']['BASELINE']/F['adeg']['BASELINE']
def save(fig,p):
    fig.savefig(p,dpi=150,bbox_inches="tight",facecolor=BG,pad_inches=.28); plt.close(fig); print("wrote",p)
def head(fig,t,s,y=1.0):
    fig.text(0,y,t,fontsize=16,weight="bold",color=INK,va="top",ha="left")
    fig.text(0,y-.052,s,fontsize=9.8,color=MUTE,va="top",ha="left")

# ---- 01 the PhD gradient, six roles ---------------------------------------
vals=[100*phd[r]/adeg[r] for r in ORDER]
fig,ax=plt.subplots(figsize=(10.4,5.4))
b=ax.barh(ORDER,vals,color=[RC[r] for r in ORDER],height=.62)
ax.axvline(base,color=MUTE,lw=1.6,ls=(0,(4,3)))
ax.annotate(f"all tech profiles  {base:.1f}%",xy=(base,-0.46),xytext=(base+1.4,-0.62),
            color=MUTE,fontsize=8.8,va="center",arrowprops=dict(arrowstyle="-",color=MUTE,lw=1))
ax.set_ylim(5.6,-0.95)
for i,(v,r) in enumerate(zip(vals,ORDER)):
    ax.text(v+.6,i,f"{v:.1f}%",va="center",fontsize=12,weight="bold",color=INK)
    ax.text(v+4.3,i,f"n={adeg[r]:,}",va="center",fontsize=8.4,color=MUTE)
ax.set_xlim(0,40); ax.set_xlabel("Share holding a PhD (%)",fontsize=9.6,color=MUTE)
ax.grid(axis="x",color=GRID,lw=.7,alpha=.75); ax.set_axisbelow(True)
ax.tick_params(length=0,labelsize=11)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
head(fig,"Six roles, one label, a 54x spread in doctorates",
     "PhD share among people listing a degree, by current role. Violet = AI roles, green = data roles.")
stamp(fig,x=.90,y=-.012,h=.036); save(fig,"01_phd_gradient.png")

# ---- 02 academic-origin share of inflow ------------------------------------
AC={"AI Researcher":(116,555),"Data Scientist":(1627,9145),"ML Engineer":(245,1456),
    "AI Engineer":(129,1266),"Data Analyst":(FD["Data Analyst"]["acad"],FD["Data Analyst"]["total"]),
    "Data Engineer":(FD["Data Engineer"]["acad"],FD["Data Engineer"]["total"])}
o2=sorted(ORDER,key=lambda r:-AC[r][0]/AC[r][1]); v2=[100*AC[r][0]/AC[r][1] for r in o2]
fig,ax=plt.subplots(figsize=(10.4,5.2))
ax.barh(o2,v2,color=[RC[r] for r in o2],height=.62)
for i,(v,r) in enumerate(zip(v2,o2)):
    ax.text(v+.3,i,f"{v:.1f}%",va="center",fontsize=12,weight="bold",color=INK)
    ax.text(v+2.2,i,f"{AC[r][1]:,} moves",va="center",fontsize=8.4,color=MUTE)
ax.set_xlim(0,27); ax.set_xlabel("Academic roles as a share of arrivals (%)",fontsize=9.6,color=MUTE)
ax.invert_yaxis(); ax.grid(axis="x",color=GRID,lw=.7,alpha=.75); ax.set_axisbelow(True)
ax.tick_params(length=0,labelsize=11)
for s in ("top","right","left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
head(fig,"Who arrives from academia — and who never does",
     "Share of each role's entry-resolved arrivals coming from Research/Teaching Assistant, Researcher, postdoc or faculty roles.")
stamp(fig,x=.90,y=-.012,h=.036); save(fig,"02_academic_share.png")

