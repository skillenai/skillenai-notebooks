"""Thirty years of tech tools, ranked — leaderboard race.

Named technologies only. A named technology is a specific artifact someone
ships and someone else adopts: a language, product, framework, platform or
service. Activities — testing, documentation, project management, CI/CD — are
excluded, because "what churns" is a question about tools, and a capability
that never had a version number cannot be replaced by the next one.

Metric is share of POSITIONS started in the trailing twelve months that name
the technology. Trailing-twelve-month windows for two reasons: a bare "2019"
start date is imputed to January, putting 17.7% of all starts there, and a
12-month window contains exactly one January so the imputation cancels; and it
removes calendar seasonality, so a partial final year does not read as a crash.

PALETTE: the validated set from the companion role race, all-pairs on #FBFCFE —
    #7A3FD1 violet | #22C1DA cyan | #E9A23B amber | #1BA36B green | MUTE
Four chromatic identities plus one neutral is the ceiling; a fifth chromatic
slot cannot clear the CVD floors, and bars reorder every frame so all-pairs is
the governing case. Role labels are colour-matched and always visible, which is
the required secondary encoding.
"""
import json, math, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

sys.path.insert(0, "/Users/jrand/git-repos/skillenai-notebooks/tech-role-pay-2026")
import brand                                     # registers Inter + brand rcParams
from brand import BG, INK, GRID, MUTE, stamp

SRC = "/Users/jrand/git-repos/skillenai-ds/work/skill-race/_out/waves.json"
W = json.load(open(SRC))
QS = [tuple(q) for q in W["quarters"]]
LAST_SOLID = tuple(W["last_solid"])
SHARE_RAW = W["share"]
POOL = W["pool"]


def key(q):
    return f"{q[0]}Q{q[1]//3}"


SHARE = {q: SHARE_RAW[key(q)] for q in QS}

# ---- display families. Four chromatic + one neutral (see palette note).
FAM = {}


def _f(name, *xs):
    for x in xs:
        FAM[x] = name


_f("Languages & runtimes", "Python", "Java", "JavaScript", "TypeScript", "C",
   "C++", "C#", "PHP", "Perl", "Ruby", "Go", "Scala", "Kotlin", "Swift", "Rust",
   "R", "MATLAB", "COBOL", "Visual Basic", "VBA", "Objective-C", "Groovy",
   ".NET", "ASP.NET", "ASP", "JSP", "J2EE", "PL/SQL", "T-SQL", "Bash",
   "PowerShell", "Shell scripting", "SAS", "Delphi", "PowerBuilder", "Assembly")
_f("Data & AI", "SQL", "MySQL", "PostgreSQL", "SQL Server", "Oracle", "Db2",
   "Sybase", "MongoDB", "Redis", "Cassandra", "Teradata", "MS Access",
   "Snowflake", "Databricks", "Redshift", "BigQuery", "Hadoop", "Spark",
   "Kafka", "Airflow", "dbt", "SSIS", "SSRS", "Excel", "Tableau", "Power BI",
   "Looker", "Qlik", "Elasticsearch", "Informatica", "Crystal Reports",
   "TensorFlow", "PyTorch", "scikit-learn", "pandas", "NumPy", "LLMs",
   "LangChain", "Hugging Face", "OpenAI")
_f("Web & frontend", "HTML", "CSS", "React", "Angular", "Vue.js", "jQuery",
   "Node.js", "XML", "Bootstrap", "Django", "Flask", "Rails", "Spring",
   "Spring Boot", "Struts", "WebSphere", "ColdFusion", "Flash", "Silverlight",
   "AJAX", "Next.js", "React Native", "Webpack", "Sass", "GraphQL", "JSON",
   "Servlets", "Figma")
_f("Infrastructure & cloud", "Linux", "Unix", "Solaris", "Windows",
   "Windows NT", "Windows Server", "AWS", "Azure", "GCP", "S3", "EC2",
   "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "Puppet", "Chef",
   "Git", "GitHub", "GitLab", "GitHub Actions", "Azure DevOps", "Subversion",
   "Active Directory", "VMware", "Citrix", "Novell", "Cisco", "Apache", "IIS",
   "Nginx", "TCP/IP")

GC = {"Languages & runtimes": "#22C1DA", "Data & AI": "#1BA36B",
      "Web & frontend": "#E9A23B", "Infrastructure & cloud": "#7A3FD1",
      "Other tools": MUTE}
fam = lambda s: FAM.get(s, "Other tools")

TOPN, FLOOR, SUB = 15, 0.03, 18
RK = {q: {s: i for i, s in enumerate(sorted(POOL, key=lambda x: -SHARE[q].get(x, 0)))}
      for q in QS}


def smooth(x):
    return x * x * (3 - 2 * x)


FRAMES = [(0, 0.0)] * 20
for i in range(len(QS) - 1):
    for k in range(SUB):
        FRAMES.append((i, k / SUB))
FRAMES += [(len(QS) - 2, 1.0)] * 75

MN = {3: "Q1", 6: "Q2", 9: "Q3", 12: "Q4"}
XMIN, XMAX = 0.045, 17.0

fig, ax = plt.subplots(figsize=(12.2, 7.0))
fig.subplots_adjust(top=.855, bottom=.135, left=.225, right=.962)
fig.text(.022, .975, "30 years of tech tools, ranked", fontsize=18.5,
         weight="bold", color=INK, va="top", ha="left")
fig.text(.022, .928,
         "Share of jobs started in the trailing 12 months naming each technology. Log scale.",
         fontsize=10.2, color=MUTE, va="top", ha="left")
date_txt = fig.text(.962, .972, "", fontsize=27, weight="bold", color=INK,
                    ha="right", va="top")
prov = fig.text(.962, .912, "", fontsize=8.6, color="#D64545", ha="right",
                va="top", style="italic")


def draw(fr):
    i, f = fr
    q0, q1 = QS[i], QS[i + 1]
    e = smooth(f)
    ax.clear()
    ax.set_xscale("log")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(TOPN - 0.3, -1.0)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_yticks([])
    ax.grid(axis="x", color=GRID, alpha=.75, lw=.7)
    ax.set_axisbelow(True)
    ax.set_xticks([.05, .1, .25, .5, 1, 2, 5, 10])
    ax.set_xticklabels(["0.05%", "0.1%", "0.25%", "0.5%", "1%", "2%", "5%", "10%"],
                       fontsize=9)
    ax.tick_params(length=0)
    ax.set_xlabel("Share of jobs started naming the technology (trailing 12 months, log scale)",
                  fontsize=9.6, color=MUTE)
    for s in POOL:
        v0 = max(SHARE[q0].get(s, 0), FLOOR)
        v1 = max(SHARE[q1].get(s, 0), FLOOR)
        v = math.exp(math.log(v0) + (math.log(v1) - math.log(v0)) * e)
        y = RK[q0][s] + (RK[q1][s] - RK[q0][s]) * e
        if y > TOPN - 0.45:
            continue
        a = 1.0 if y <= TOPN - 1.45 else max(0.0, (TOPN - 0.45 - y))
        if a <= .02:
            continue
        col = GC[fam(s)]
        ax.barh(y, v, height=.68, color=col, alpha=a)
        ax.text(-0.012, y, s, ha="right", va="center", fontsize=10.2,
                weight="semibold", color=col, alpha=a, clip_on=False,
                transform=ax.get_yaxis_transform())
        ax.text(v * 1.06, y, f"{v:.2f}%", va="center", fontsize=9.4,
                weight="bold", color=INK, alpha=a)
    cur = q0 if e < .5 else q1
    date_txt.set_text(f"{MN[cur[1]]} {cur[0]}")
    prov.set_text("provisional - reporting lag" if cur > LAST_SOLID else "")
    return []


h = [plt.Rectangle((0, 0), 1, 1, color=GC[g]) for g in GC]
fig.legend(h, list(GC), loc="lower center", ncol=5, frameon=False, fontsize=9.6,
           bbox_to_anchor=(.50, .002))
stamp(fig, x=.878, y=.012, h=.040)

ani = FuncAnimation(fig, draw, frames=FRAMES, blit=False)
ani.save("01_tool_race.mp4",
         writer=FFMpegWriter(fps=30, bitrate=3400, extra_args=["-pix_fmt", "yuv420p"]),
         dpi=100)
print(f"wrote 01_tool_race.mp4  {len(FRAMES)}f @30fps = {len(FRAMES)/30:.0f}s  "
      f"{os.path.getsize('01_tool_race.mp4')/1048576:.1f} MB")
fin = SHARE[QS[-1]]
top = sorted(POOL, key=lambda s: -fin.get(s, 0))[:8]
print("final board: " + ", ".join(f"{s} {fin[s]:.2f}%" for s in top))
