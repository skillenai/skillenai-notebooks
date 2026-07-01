"""
Generate figures for the AI Engineer talent-flow analysis.
Data sources: Live Data Technologies (supply / profiles) + Skillenai (demand / postings).
All numbers are hard-coded from the exploratory queries so the script is self-contained
and reproducible without re-hitting the APIs. See README.md for methodology.
"""
import csv
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

mpl.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
})

HERE = os.path.dirname(os.path.abspath(__file__))
def out(name): return os.path.join(HERE, name)

# Skillenai brand-ish palette
C = {
    "AIE": "#2563eb",   # blue  (protagonist)
    "DS":  "#dc2626",   # red   (the stall)
    "MLE": "#7c3aed",   # purple
    "DE":  "#0d9488",   # teal
    "SWE": "#64748b",   # slate
    "grid": "#e5e7eb",
    "ink": "#111827",
}

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
YEARS = list(range(2012, 2026))  # full years only (2026 is partial)

NET = {  # annual net additions (arrivals - departures), Live Data
    "AIE": [75, 103, 161, 259, 497, 795, 1272, 1419, 1661, 2671, 3127, 4486, 8184, 11769],
    "DS":  [2037, 3133, 5006, 7279, 9145, 11571, 13997, 14652, 9773, 11221, 9299, 2504, 203, -107],
    "MLE": [223, 325, 491, 892, 1657, 2705, 3922, 4527, 4367, 5139, 4323, 2407, 3074, 2538],
    "DE":  [2387, 3260, 4310, 5752, 6986, 9085, 11792, 13614, 12622, 22242, 18850, 8102, 5519, 5642],
}

# arrivals vs departures over 2023-01..2026-06 (Live Data), for the in:out ratio
INOUT = {  # role: (arrivals, departures)
    "AIE": (60078, 30451),
    "MLE": (43305, 35857),
    "DE":  (121059, 104082),
    "SWE": (720976, 680536),
    "DS":  (80120, 78458),
}
INOUT_LABEL = {"AIE": "AI Engineer", "MLE": "ML Engineer", "DE": "Data Engineer",
               "SWE": "Software Engineer", "DS": "Data Scientist"}

# AI-native skill prevalence in postings (Skillenai), % of role's postings
SKILLS = ["LLM", "Agentic", "Prompt eng.", "LangChain", "RAG", "Fine-tuning",
          "PyTorch", "MLOps", "Statistics"]
SKILL_VALS = {
    "AIE": [49.7, 39.2, 24.9, 19.6, 13.9, 20.5, 16.4, 12.1, 5.3],
    "MLE": [21.0, 13.4, 6.4, 4.9, 4.3, 13.8, 38.6, 16.9, 12.6],
    "DS":  [10.5, 7.7, 3.4, 3.5, 2.2, 3.4, 12.1, 8.1, 37.2],
    "SWE": [7.2, 8.3, 2.2, 1.4, 0.9, 1.2, 1.8, 1.1, 0.9],
}

# Salary median band (USD), Skillenai
SAL = {  # role: (median_min, median_max)
    "MLE": (171960, 248688),
    "AIE": (159659, 220104),
    "SWE": (155326, 218376),
    "DS":  (145199, 201261),
}

# Sankey flows (Live Data samples). Inflow n=56 resolved, outflow n=40 resolved.
INFLOW = [
    ("Software Engineer", 10, "SWE"),
    ("Other engineering", 8, "MLE"),
    ("ML Engineer", 8, "MLE"),
    ("Founder / Leadership", 8, "FND"),
    ("Data Sci / Analytics", 7, "DS"),
    ("Product / Manager", 5, "PM"),
    ("Student / Intern", 2, "STU"),
    ("Other", 8, "OTH"),
]
OUTFLOW = [
    ("Founder / Leadership", 9, "FND"),
    ("ML Engineer", 5, "MLE"),
    ("Researcher / Scientist", 5, "RES"),
    ("Software Engineer", 5, "SWE"),
    ("Data Scientist", 4, "DS"),
    ("Other engineering", 5, "MLE"),
    ("Manager / Product", 2, "PM"),
    ("Other", 5, "OTH"),
]
SANKEY_COLORS = {"SWE": "#64748b", "MLE": "#7c3aed", "DS": "#dc2626", "FND": "#ea580c",
                 "PM": "#0891b2", "STU": "#a3a3a3", "RES": "#16a34a", "OTH": "#cbd5e1"}

# ---------------------------------------------------------------------------
# write CSVs (small, committable)
# ---------------------------------------------------------------------------
def write_csvs():
    with open(out("net_flow_by_role.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["year", "AI_Engineer", "Data_Scientist", "ML_Engineer", "Data_Engineer"])
        for i, y in enumerate(YEARS):
            w.writerow([y, NET["AIE"][i], NET["DS"][i], NET["MLE"][i], NET["DE"][i]])
    with open(out("inout_ratio.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["role", "arrivals", "departures", "in_out_ratio"])
        for r, (a, d) in INOUT.items():
            w.writerow([INOUT_LABEL[r], a, d, round(a/d, 3)])
    with open(out("skill_prevalence.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["skill", "AI_Engineer", "ML_Engineer", "Data_Scientist", "Software_Engineer"])
        for i, s in enumerate(SKILLS):
            w.writerow([s, SKILL_VALS["AIE"][i], SKILL_VALS["MLE"][i], SKILL_VALS["DS"][i], SKILL_VALS["SWE"][i]])

# ---------------------------------------------------------------------------
# FIG 1 — net-flow handoff
# ---------------------------------------------------------------------------
def fig_handoff():
    fig, ax = plt.subplots(figsize=(10, 6))
    order = [("DS", "Data Scientist"), ("DE", "Data Engineer"), ("MLE", "ML Engineer"), ("AIE", "AI Engineer")]
    for key, lab in order:
        lw = 3.4 if key in ("AIE", "DS") else 1.8
        alpha = 1.0 if key in ("AIE", "DS") else 0.55
        ax.plot(YEARS, NET[key], color=C[key], lw=lw, alpha=alpha, marker="o",
                ms=5 if key in ("AIE", "DS") else 3, label=lab, zorder=3 if key in ("AIE","DS") else 2)
    ax.axhline(0, color=C["ink"], lw=0.8, ls="--", alpha=0.5)
    ax.axvspan(2022.5, 2025.5, color="#f3f4f6", zorder=0)
    ax.text(2024, 15900, "post-2022\nhiring freeze", ha="center", va="top", fontsize=9, color="#6b7280")
    ax.axvline(2020, color="#9ca3af", lw=1, ls=":", alpha=0.7, zorder=1)
    ax.text(2020, 16200, "COVID", ha="center", fontsize=8.5, color="#9ca3af")
    # annotate key points
    ax.annotate("Data Scientist peak\n+14,652 (2019)", (2019, 14652), color=C["DS"], fontsize=9,
                xytext=(2013.2, 15200), va="center", ha="left")
    ax.annotate("+11,769", (2025, 11769), color=C["AIE"], fontweight="bold", fontsize=11, xytext=(6,0), textcoords="offset points", va="center")
    ax.annotate("−107", (2025, -107), color=C["DS"], fontweight="bold", fontsize=11, xytext=(6,-2), textcoords="offset points", va="center")
    ax.set_title("The handoff: AI Engineer accelerates as Data Scientist stalls out", pad=14)
    ax.set_ylabel("Net people added to the role per year\n(arrivals − departures)")
    ax.set_xlabel("Year")
    ax.set_xticks(YEARS[::2] + [2025])
    ax.grid(axis="y", color=C["grid"], lw=0.7)
    ax.legend(loc="upper left", frameon=False, fontsize=11)
    ax.set_ylim(-2000, 16500)
    fig.text(0.5, -0.02, "Source: Live Data Technologies (95M+ profiles). Net flow = new title-holders minus departures. 2026 excluded (partial year).",
             ha="center", fontsize=8, color="#9ca3af")
    fig.tight_layout()
    fig.savefig(out("01_net_flow_handoff.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 2 — in:out ratio
# ---------------------------------------------------------------------------
def fig_ratio():
    roles = sorted(INOUT, key=lambda r: INOUT[r][0]/INOUT[r][1])
    ratios = [INOUT[r][0]/INOUT[r][1] for r in roles]
    labels = [INOUT_LABEL[r] for r in roles]
    colors = [C[r] if r in ("AIE", "DS") else "#cbd5e1" for r in roles]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(labels, ratios, color=colors, edgecolor="white")
    ax.axvline(1.0, color=C["ink"], ls="--", lw=1, alpha=0.6)
    ax.text(1.03, len(roles)-0.42, "1.0 = replacement\n(one leaves per hire)", fontsize=9, color="#6b7280", ha="left", va="center")
    for b, r in zip(bars, ratios):
        ax.text(b.get_width()+0.02, b.get_y()+b.get_height()/2, f"{r:.2f}×", va="center", fontweight="bold", fontsize=11)
    ax.set_title("AI Engineer is the only role hiring ~2-for-1", pad=12)
    ax.set_xlabel("Arrivals per departure, 2023–2026 (Live Data)")
    ax.set_xlim(0, 2.25)
    ax.set_ylim(-0.6, len(roles)-0.1)
    ax.grid(axis="x", color=C["grid"], lw=0.7)
    fig.tight_layout()
    fig.savefig(out("02_inout_ratio.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 3 — skill fingerprint
# ---------------------------------------------------------------------------
def fig_skills():
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(SKILLS)); w = 0.2
    for i, (key, lab) in enumerate([("AIE","AI Engineer"),("MLE","ML Engineer"),("DS","Data Scientist"),("SWE","Software Engineer")]):
        ax.bar(x + (i-1.5)*w, SKILL_VALS[key], w, label=lab, color=C[key], edgecolor="white", linewidth=0.4)
    ax.set_title("Different job, not a rename: the AI Engineer skill fingerprint", pad=12)
    ax.set_ylabel("% of the role's postings mentioning the skill")
    ax.set_xticks(x); ax.set_xticklabels(SKILLS, rotation=25, ha="right")
    ax.legend(frameon=False, ncol=4, loc="upper right", fontsize=10)
    ax.grid(axis="y", color=C["grid"], lw=0.7)
    fig.text(0.5, -0.03, "Source: Skillenai job-postings index. AI Engineer dominates the LLM/agent/RAG stack; ML Eng owns PyTorch/MLOps; Data Scientist owns statistics.",
             ha="center", fontsize=8, color="#9ca3af")
    fig.tight_layout()
    fig.savefig(out("03_skill_fingerprint.png"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 4 — Sankey (hand-built)
# ---------------------------------------------------------------------------
def _rgba(hexc, a):
    h = hexc.lstrip("#")
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"

def fig_sankey():
    import plotly.graph_objects as go
    in_tot = sum(v for _, v, _ in INFLOW)
    out_tot = sum(v for _, v, _ in OUTFLOW)
    n_in = len(INFLOW)
    center = n_in

    labels, colors, node_x, node_y = [], [], [], []
    for name, val, ck in INFLOW:
        labels.append(f"{name}  ({100*val/in_tot:.0f}%)"); colors.append(SANKEY_COLORS[ck]); node_x.append(0.001)
    labels.append("AI ENGINEER"); colors.append(C["AIE"]); node_x.append(0.5)
    for name, val, ck in OUTFLOW:
        labels.append(f"{name}  ({100*val/out_tot:.0f}%)"); colors.append(SANKEY_COLORS[ck]); node_x.append(0.999)
    # even vertical spacing per column
    for i in range(n_in):       node_y.append((i + 0.5) / n_in)
    node_y.append(0.5)
    for j in range(len(OUTFLOW)): node_y.append(0.28 + 0.44 * (j + 0.5) / len(OUTFLOW))

    src, tgt, valv, lcol = [], [], [], []
    # inflow scaled to total 2.0, outflow to 1.0  -> inflow band ~2x (the ~2:1 arrivals:departures)
    for i, (_, val, ck) in enumerate(INFLOW):
        src.append(i); tgt.append(center); valv.append(2.0 * val / in_tot); lcol.append(_rgba(SANKEY_COLORS[ck], 0.45))
    for j, (_, val, ck) in enumerate(OUTFLOW):
        src.append(center); tgt.append(center + 1 + j); valv.append(1.0 * val / out_tot); lcol.append(_rgba(SANKEY_COLORS[ck], 0.45))

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=labels, color=colors, x=node_x, y=node_y, pad=14, thickness=16,
                  line=dict(width=0)),
        link=dict(source=src, target=tgt, value=valv, color=lcol),
    ))
    fig.update_layout(
        title=dict(text="<b>Who becomes an AI Engineer — and where they go next</b>",
                   x=0.5, font=dict(size=20, color=C["ink"])),
        font=dict(family="DejaVu Sans", size=13, color=C["ink"]),
        annotations=[
            dict(x=0.001, y=1.09, xref="paper", yref="paper", showarrow=False,
                 text="<b>WHERE THEY COME FROM</b>", font=dict(size=12, color="#374151")),
            dict(x=0.999, y=1.09, xref="paper", yref="paper", showarrow=False,
                 text="<b>WHERE THEY GO</b>", font=dict(size=12, color="#374151")),
            dict(x=0.5, y=-0.14, xref="paper", yref="paper", showarrow=False,
                 text="Source: Live Data Technologies career histories (directional sample: inflow n=56, outflow n=40).  "
                      "Inflow drawn ~2× outflow, reflecting the ~2:1 arrivals-to-departures ratio.",
                 font=dict(size=10, color="#9ca3af")),
        ],
        margin=dict(l=10, r=10, t=90, b=70), width=1150, height=680, paper_bgcolor="white",
    )
    fig.write_image(out("04_sankey_flows.png"), scale=2)

# ---------------------------------------------------------------------------
# FIG 5 — salary
# ---------------------------------------------------------------------------
def fig_salary():
    roles = ["MLE", "AIE", "SWE", "DS"]
    labels = ["ML Engineer", "AI Engineer", "Software Engineer", "Data Scientist"]
    lows = [SAL[r][0] for r in roles]; highs = [SAL[r][1] for r in roles]
    mids = [(l+h)/2 for l, h in zip(lows, highs)]
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(roles))[::-1]
    for yi, r, lo, hi, m in zip(y, roles, lows, highs, mids):
        ax.plot([lo/1000, hi/1000], [yi, yi], color=C[r], lw=8, solid_capstyle="round", alpha=0.85)
        ax.plot(m/1000, yi, "o", color="white", ms=7, markeredgecolor=C[r], markeredgewidth=2)
        ax.text(hi/1000+4, yi, f"${m/1000:.0f}k mid", va="center", fontsize=10, color=C["ink"])
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("USD salary band (median min → median max, thousands)")
    ax.set_title("AI Engineer pays like a premium software engineer", pad=12)
    ax.grid(axis="x", color=C["grid"], lw=0.7)
    ax.set_xlim(120, 285)
    fig.tight_layout()
    fig.savefig(out("05_salary_band.png"), bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    write_csvs()
    fig_handoff(); fig_ratio(); fig_skills(); fig_sankey(); fig_salary()
    print("wrote figures + csvs to", HERE)
