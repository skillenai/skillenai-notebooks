"""Render the chart and verify published statistics from aggregate cohorts.csv."""
import csv,math,pathlib,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/skn-founder-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
for f in (ROOT/'fonts').glob('*.ttf'):font_manager.fontManager.addfont(str(f))
if any((ROOT/'fonts').glob('*.ttf')):plt.rcParams['font.family']=font_manager.FontProperties(fname=str(next((ROOT/'fonts').glob('*400.ttf')))).get_name()
INK='#16233F';BLUE='#2E7FD1';VIOLET='#7A3FD1';BG='#FBFCFE'
rows=list(csv.DictReader(open(ROOT/'cohorts.csv')))
rows=[r for r in rows if r['cohort']=='all_founder_starters']
def wilson(k,n):
 p=k/n;z=1.96;den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return 100*(c-h),100*(c+h)
years=[int(r['year']) for r in rows];n=[int(r['founder_starters']) for r in rows];k=[int(r['operating_prior_overlap']) for r in rows]
p=[100*a/b for a,b in zip(k,n)];ci=[wilson(a,b) for a,b in zip(k,n)]
fig,ax=plt.subplots(figsize=(12.8,7.2),facecolor=BG);ax.set_facecolor(BG)
fig.subplots_adjust(left=.095,right=.94,bottom=.23,top=.72)
fig.text(.075,.92,'Starting a venture while another job continues',fontsize=24,color=INK,weight='semibold')
fig.text(.075,.85,'Share of founder starters already holding an operating role at another organization',fontsize=13,color=INK)
fig.text(.075,.80,'January–July cohorts · US tech/AI-headline profile sample · bars show 95% intervals',fontsize=11,color='#627087')
ax.errorbar(years,p,yerr=[[v-lo for v,(lo,hi) in zip(p,ci)],[hi-v for v,(lo,hi) in zip(p,ci)]],color=BLUE,elinewidth=1.3,capsize=4,linewidth=2.6,marker='o',markersize=8,zorder=3)
for year,v,(_,hi) in zip(years,p,ci):ax.annotate(f'{v:.1f}%',(year,hi),xytext=(0,9),textcoords='offset points',ha='center',fontsize=12,color=INK,weight='semibold')
ax.set_ylim(25,63);ax.set_yticks([30,40,50,60],['30%','40%','50%','60%']);ax.set_xlim(2017.7,2025.3)
ax.set_xticks(years,[f'{y}\nn={nn:,}' for y,nn in zip(years,n)],fontsize=10,color=INK)
ax.grid(axis='y',color='#DFE6EF',linewidth=.8);ax.set_axisbelow(True);ax.tick_params(length=0,pad=10,colors=INK)
for sp in ax.spines.values():sp.set_visible(False)
fig.text(.075,.115,'2023–2025: +4.0 percentage points; approximate 95% interval −1.0 to +9.1.',fontsize=12,color=INK)
fig.text(.075,.066,'Source: Skillenai career histories, July–September 2026 snapshots.\nRecorded overlap; hours, pay, remote work, and AI use are not observed.',fontsize=9,color='#627087',va='top')
stamp=ROOT/'logo_stamp.png'
if stamp.exists():
 logo=Image.open(stamp);la=fig.add_axes([.825,.028,.036,.064]);la.imshow(logo);la.axis('off');fig.text(.867,.045,'Skillenai',fontsize=14,color='#6c6c6c')
else:fig.text(.94,.045,'Skillenai',fontsize=15,color='#6c6c6c',ha='right')
fig.savefig(ROOT/'founder-overlap.png',dpi=150,facecolor=BG)
for y,kk,nn in zip(years,k,n):print(y,kk,nn,round(100*kk/nn,3),wilson(kk,nn))
