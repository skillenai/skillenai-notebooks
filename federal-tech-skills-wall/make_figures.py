import pandas as pd, json, re, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

plt.rcParams.update({"font.size": 11, "axes.sppines" if False else "axes.grid": True,
                     "axes.axisbelow": True, "grid.alpha": .25, "figure.dpi": 150})
FED_C = "#c0392b"   # federal red
PRIV_C = "#2471a3"  # private blue
OUT = "."  # writes PNGs to cwd

fed = pd.read_parquet("federal_tech_hf.parquet")
fed['tl'] = fed.title.str.lower()
priv = {k: [(h.get("extractedText") or "") for h in json.load(open(f"private_{k}.json"))]
        for k in ["ds", "swe", "sec"]}

def rate(texts, pat):
    rx = re.compile(pat, re.I); n = len(texts)
    return 100*sum(1 for t in texts if rx.search(t))/n if n else 0

def fedsub(mask): return list(fed[mask].duties)
FDS = fedsub(fed.tl.str.contains("data scientist|data science") | fed.series.isin(["1560"]))
FSWE = fedsub((fed.series.isin(["2210","1550"])) & fed.tl.str.contains("software|developer|programmer|application|appsw|full stack|web "))
FSEC = fedsub(fed.tl.str.contains("cyber|security|infosec|information security|information assurance"))

import os
os.makedirs(OUT, exist_ok=True)

# ---------- FIG 1: the missing roles (headline) ----------
fig, ax = plt.subplots(figsize=(9, 5.2))
roles = ["Data\nScientist", "Data\nAnalyst", "Data\nEngineer", "ML\nEngineer", "AI\nEngineer"]
fed_ct = [99, 22, 6, 1, 2]           # federal titles across 84,016 postings (6 mo)
priv_ct = [2181, 1038, 1758, 2555, 848]  # private index counts
x = np.arange(len(roles)); w = .4
ax.bar(x-w/2, fed_ct, w, color=FED_C, label="Federal (84,016 postings, 6 mo)")
ax.bar(x+w/2, priv_ct, w, color=PRIV_C, label="Private (Skillenai index)")
ax.set_yscale("log"); ax.set_ylim(0.5, 2e4)
ax.set_ylabel("Job postings (log scale)")
ax.set_title("The modern data org barely exists in federal hiring\nFederal counts (6 mo, all 84,016 postings) vs private-market counts", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(roles)
for i, (f, p) in enumerate(zip(fed_ct, priv_ct)):
    ax.text(i-w/2, f*1.2, str(f), ha="center", fontsize=9, color=FED_C, fontweight="bold")
    ax.text(i+w/2, p*1.2, f"{p:,}", ha="center", fontsize=9, color=PRIV_C, fontweight="bold")
ax.legend(loc="upper left", framealpha=.95); ax.grid(axis="x")
plt.tight_layout(); plt.savefig(f"{OUT}/01_missing_roles.png", bbox_inches="tight"); plt.close()

# ---------- FIG 2: federal DS vs private DS stack divergence ----------
DS_PROBES = [
    ("Statistics", r"statistic"), ("Data visualization", r"data visualiz|visualization"),
    ("Dashboards / reporting", r"dashboard|reporting|business intelligence"),
    ("Tableau / Power BI", r"tableau|power ?bi|qlik"), ("SAS / SPSS", r"\bsas\b|\bspss\b"),
    ("\"Machine learning\"", r"machine learning"),
    ("Python", r"\bpython\b"), ("Experimentation / A-B / causal", r"a/b test|experimentation|causal infer"),
    ("MLOps / deployment / pipeline", r"deploy|mlops|production model|data pipeline"),
    ("Cloud (AWS/GCP/Azure)", r"\baws\b|\bgcp\b|\bazure\b|google cloud"),
    ("LLM / GenAI", r"\bllm\b|large language|generative ai"),
]
labels = [p[0] for p in DS_PROBES]
fedv = [rate(FDS, p[1]) for p in DS_PROBES]
prv = [rate(priv["ds"], p[1]) for p in DS_PROBES]
y = np.arange(len(labels))[::-1]
fig, ax = plt.subplots(figsize=(9.5, 6.4))
ax.barh(y+.2, fedv, .4, color=FED_C, label=f"Federal DS (N={len(FDS)})")
ax.barh(y-.2, prv, .4, color=PRIV_C, label=f"Private DS (N={len(priv['ds'])})")
ax.set_yticks(y); ax.set_yticklabels(labels)
ax.xaxis.set_major_formatter(PercentFormatter())
ax.set_xlabel("% of postings mentioning")
ax.set_title("Same title, different job: the federal Data Scientist\nStatistics-and-reporting (top) vs code-experiment-deploy (bottom)", fontweight="bold")
ax.axhline(5.5, color="k", lw=.8, ls="--", alpha=.5)
ax.legend(loc="lower right")
for yi, f, p in zip(y, fedv, prv):
    ax.text(f+1, yi+.2, f"{f:.0f}", va="center", fontsize=8, color=FED_C)
    ax.text(p+1, yi-.2, f"{p:.0f}", va="center", fontsize=8, color=PRIV_C)
plt.tight_layout(); plt.savefig(f"{OUT}/02_ds_stack_divergence.png", bbox_inches="tight"); plt.close()

# ---------- FIG 3: role composition (families + series) ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fams = ["Software/Dev", "Data/ML/AI", "Security/Cyber", "IT/Ops/Infra", "Program/Product/Mgmt"]
fed_share = [6.4, 8.9, 25.3, 42.3, 17.2]
priv_share = [43.2, 18.4, 3.1, 12.3, 23.1]
yy = np.arange(len(fams))[::-1]
ax = axes[0]
ax.barh(yy+.2, fed_share, .4, color=FED_C, label="Federal tech")
ax.barh(yy-.2, priv_share, .4, color=PRIV_C, label="Private tech")
ax.set_yticks(yy); ax.set_yticklabels(fams)
ax.xaxis.set_major_formatter(PercentFormatter())
ax.set_xlabel("Share of tech postings")
ax.set_title("Role families invert between sectors", fontweight="bold")
ax.legend()
for yi, f, p in zip(yy, fed_share, priv_share):
    ax.text(f+.6, yi+.2, f"{f:.0f}%", va="center", fontsize=8, color=FED_C)
    ax.text(p+.6, yi-.2, f"{p:.0f}%", va="center", fontsize=8, color=PRIV_C)
# right: series 2210 dominance donut-ish bar
ax = axes[1]
sers = ["2210 IT Mgmt", "1560 Data Science", "0855 Electronics", "1515 Ops Research",
        "1550 Comp Science", "0854 Comp Eng", "1530/1529 Stats"]
vals = [83.3, 3.4, 3.4, 3.0, 2.6, 2.3, 1.9]
colors = [FED_C] + ["#e59866"]*6
ax.barh(np.arange(len(sers))[::-1], vals, color=colors)
ax.set_yticks(np.arange(len(sers))[::-1]); ax.set_yticklabels(sers)
ax.xaxis.set_major_formatter(PercentFormatter())
ax.set_xlabel("Share of federal tech postings")
ax.set_title("One OPM series (2210) is 83% of federal tech\n\"Data Science\" (1560) is 3.4%", fontweight="bold")
for i, v in zip(np.arange(len(sers))[::-1], vals):
    ax.text(v+1, i, f"{v:.0f}%", va="center", fontsize=9, fontweight="bold")
plt.tight_layout(); plt.savefig(f"{OUT}/03_role_composition.png", bbox_inches="tight"); plt.close()

# ---------- FIG 4: SWE + Security stack divergence ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
SWE_P = [("COBOL", r"\bcobol\b"), ("Visual Basic", r"visual basic|vb\.net"), ("PHP", r"\bphp\b"),
         ("RMF / NIST / FISMA", r"\brmf\b|\bnist\b|fisma|fedramp|risk management framework"),
         ("Security clearance", r"security clearance|clearance"),
         ("Python", r"\bpython\b"), ("AWS", r"\baws\b|amazon web services"),
         ("Kubernetes / Docker", r"kubernetes|k8s|\bdocker\b"), ("TypeScript", r"typescript"),
         ("CI/CD / microservices", r"ci/cd|microservice")]
SEC_P = [("Security clearance", r"security clearance|clearance"), ("RMF / A&A / ATO", r"\brmf\b|authorization to operate|assessment and authorization"),
         ("NIST", r"\bnist\b"),
         ("Python", r"\bpython\b"), ("AWS / GCP", r"\baws\b|\bgcp\b|google cloud"),
         ("Kubernetes / Terraform", r"kubernetes|terraform"), ("Threat modeling", r"threat model"),
         ("SIEM", r"\bsiem\b"), ("CI/CD", r"ci/cd|continuous integration"),
         ("Penetration testing", r"penetration test|pen[- ]?test")]
for ax, probes, ftx, ptx, title, tag in [
    (axes[0], SWE_P, FSWE, priv["swe"], f"Software Engineer\nlegacy+compliance (fed) vs cloud-native (priv)", "swe"),
    (axes[1], SEC_P, FSEC, priv["sec"], f"Cybersecurity\nclearance+governance (fed) vs hands-on (priv)", "sec")]:
    labs = [p[0] for p in probes]
    fv = [rate(ftx, p[1]) for p in probes]; pv = [rate(ptx, p[1]) for p in probes]
    yy = np.arange(len(labs))[::-1]
    ax.barh(yy+.2, fv, .4, color=FED_C, label=f"Federal (N={len(ftx)})")
    ax.barh(yy-.2, pv, .4, color=PRIV_C, label=f"Private (N={len(ptx)})")
    ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=9)
    ax.xaxis.set_major_formatter(PercentFormatter())
    ax.set_title(title, fontweight="bold"); ax.legend(loc="lower right", fontsize=8)
    ax.axhline(4.5, color="k", lw=.8, ls="--", alpha=.4)
plt.tight_layout(); plt.savefig(f"{OUT}/04_swe_security_stacks.png", bbox_inches="tight"); plt.close()

# ---------- FIG 5: the other walls — clearance + remote ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
fams2 = ["Security/Cyber", "IT/Ops/Infra", "Program/Mgmt", "Data/ML/AI", "Software/Dev", "ALL federal tech"]
clr = [85, 69, 66, 60, 37, 70]
ax.barh(np.arange(len(fams2))[::-1], clr, color=FED_C)
ax.axvline(np.mean([4, 12]), color=PRIV_C, ls="--", lw=1.5)
ax.text(9, 0.2, "private ~4–12%", color=PRIV_C, fontsize=9, rotation=90, va="bottom")
ax.set_yticks(np.arange(len(fams2))[::-1]); ax.set_yticklabels(fams2)
ax.xaxis.set_major_formatter(PercentFormatter())
ax.set_title("The clearance wall\n% of federal postings requiring a real clearance", fontweight="bold")
for i, v in zip(np.arange(len(fams2))[::-1], clr):
    ax.text(v+1, i, f"{v:.0f}%", va="center", fontsize=9, fontweight="bold")
ax.set_title("The clearance wall\n% of federal tech postings requiring a clearance", fontweight="bold", fontsize=11)
ax = axes[1]
trend = json.load(open("remote_trend.json"))  # [(month, remote_yes_pct), ...]
labels_t = [m for m, _ in trend]; vals_t = [v for _, v in trend]
xt = np.arange(len(trend))
ax.plot(xt, vals_t, "-o", color=FED_C, lw=2, ms=5)
rto = labels_t.index("2025-01")
ax.axvline(rto, color="k", ls="--", lw=1, alpha=.6)
ax.text(rto+.15, 9.7, "Jan 2025\nfederal RTO order", fontsize=8, va="top")
ax.text(0.2, 10.3, "(private tech ~31% fully-remote — off scale)", color=PRIV_C, fontsize=8.5, va="top")
ax.set_xticks(xt); ax.set_xticklabels(labels_t, rotation=60, ha="right", fontsize=7.5)
ax.yaxis.set_major_formatter(PercentFormatter()); ax.set_ylim(-0.5, 11)
ax.set_ylabel("% of federal tech postings\ndesignated remote")
ax.set_title("The remote door slammed shut\nFederal remote hiring: ~8% → 0.3% after RTO mandate", fontweight="bold", fontsize=11)
ax.annotate("0.3%", (len(trend)-1, vals_t[-1]), textcoords="offset points", xytext=(-4, 11),
            fontsize=9, color=FED_C, fontweight="bold")
plt.subplots_adjust(wspace=0.28); plt.tight_layout(); plt.savefig(f"{OUT}/05_other_walls.png", bbox_inches="tight"); plt.close()
print("figures written to", OUT)
import glob
for f in sorted(glob.glob(f"{OUT}/*.png")):
    print(" ", os.path.basename(f), os.path.getsize(f)//1024, "KB")
