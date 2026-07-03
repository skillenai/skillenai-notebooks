"""Figures for the federal-tech 'broken bargain' analysis."""
import json, pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "font.family": "DejaVu Sans"})
NAVY, TEAL, CORAL, GOLD, GREY = "#1b2a4a", "#2a9d8f", "#e76f51", "#e9c46a", "#8d99ae"
usd = FuncFormatter(lambda x, _: f"${x/1000:.0f}K")

pay = pd.read_csv("federal_pay.csv")
sen = pd.read_csv("federal_seniority.csv")
stab = pd.read_csv("federal_stability.csv")
B = json.load(open("private_and_bls.json"))

# ---------- FIG 1: Pay — federal vs private, the ceiling ----------
fig, ax = plt.subplots(figsize=(11, 6))
roles = ["Data Scientist", "Software Engineer"]
fed_map = {"Data Scientist": "Data Scientist", "Software Engineer": "Software Engineer / IT"}
y = np.arange(len(roles)); h = 0.36
for i, r in enumerate(roles):
    fp = pay[pay.role == fed_map[r]].iloc[0]
    pv = B["private_posted_salary_us_usd"][r]
    # private posted band (min_p50 -> max_p50)
    ax.barh(y[i] + h/2, pv["max_p50"] - pv["min_p50"], left=pv["min_p50"], height=h,
            color=TEAL, alpha=.85, label="Private posted band (p50 min→max)" if i == 0 else "")
    ax.plot((pv["min_p50"]+pv["max_p50"])/2, y[i]+h/2, "o", color=NAVY, ms=7,
            label="Private midpoint" if i == 0 else "")
    # federal new-hire p25->p75 with p50 marker
    ax.barh(y[i] - h/2, fp.newhire_p75 - fp.newhire_p25, left=fp.newhire_p25, height=h,
            color=CORAL, alpha=.85, label="Federal new-hire band (p25→p75)" if i == 0 else "")
    ax.plot(fp.newhire_p50, y[i]-h/2, "s", color=NAVY, ms=7,
            label="Federal new-hire median" if i == 0 else "")
ax.axvline(197200, color=GREY, ls="--", lw=1.5)
ax.text(199500, 0.5, "GS-15 ceiling\n(~$197K, locality-adj.)\nfederal base caps here;\nprivate has no ceiling",
        va="center", ha="left", fontsize=8.5, color="#4a4a4a")
ax.set_yticks(y); ax.set_yticklabels(roles); ax.xaxis.set_major_formatter(usd)
ax.set_xlabel("Annual base pay (USD)")
ax.set_title("The federal tech pay penalty\nFederal new-hire base vs private posted base — before equity or bonus",
             fontweight="bold", loc="left")
ax.legend(loc="lower right", fontsize=9, framealpha=.95)
ax.set_xlim(80000, 260000)
plt.tight_layout(); plt.savefig("01_pay_gap.png", bbox_inches="tight"); plt.close()

# ---------- FIG 2: Seniority — the missing junior rung ----------
fig, ax = plt.subplots(figsize=(10, 5.2))
cats = ["Data Scientist", "Software Engineer"]
fed_map2 = {"Data Scientist": "Data Scientist", "Software Engineer": "Software Engineer / IT"}
labels, entry, mid, senior, sides = [], [], [], [], []
for r in cats:
    fs = sen[sen.role == fed_map2[r]].iloc[0]
    labels.append(f"Federal\n{r}"); entry.append(fs.entry_pct); mid.append(fs.mid_pct); senior.append(fs.senior_pct)
    pv = B["private_seniority_pct"][r]
    labels.append(f"Private\n{r}"); entry.append(pv["entry"]); mid.append(pv["mid"]); senior.append(pv["senior_plus"])
yy = np.arange(len(labels))
ax.barh(yy, entry, color=GOLD, label="Entry (≤GS-9 / entry+intern)")
ax.barh(yy, mid, left=entry, color=TEAL, label="Mid (GS-11/12 / mid)")
ax.barh(yy, senior, left=np.array(entry)+np.array(mid), color=NAVY, label="Senior+ (GS-13+ / senior…principal)")
for i in range(len(labels)):
    if entry[i] >= 2.5: ax.text(entry[i]/2, yy[i], f"{entry[i]:.0f}%", va="center", ha="center", color="#4a4a4a", fontsize=9)
    else: ax.text(entry[i], yy[i], f" {entry[i]:.0f}%", va="center", ha="left", color=CORAL, fontsize=9, fontweight="bold")
ax.set_yticks(yy); ax.set_yticklabels(labels, fontsize=9.5); ax.invert_yaxis()
ax.set_xlabel("Share of workforce (%)"); ax.set_xlim(0, 100)
ax.set_title("The missing junior rung\nFederal tech is a steeper 'senior club' than private industry",
             fontweight="bold", loc="left")
ax.legend(loc="lower right", fontsize=8.5, framealpha=.95)
plt.tight_layout(); plt.savefig("02_seniority.png", bbox_inches="tight"); plt.close()

# ---------- FIG 3: Stability — the revocable bargain ----------
fig, ax = plt.subplots(figsize=(12, 5.6))
stab["date"] = pd.to_datetime(stab.month + "-01")
ax.plot(stab.date, stab.quit_rate_ann_pct, color=NAVY, lw=2, marker="o", ms=3, label="Federal tech (OPM FWD)")
# BLS annualized reference lines (monthly ×12)
j = B["bls_jolts_quits_rate_monthly_pct_may2026"]
ax.axhline(j["total_private"]*12, color=CORAL, ls="--", lw=1.5, label=f"Total private (BLS JOLTS ≈{j['total_private']*12:.0f}%/yr)")
ax.axhline(j["information"]*12, color=TEAL, ls="--", lw=1.5, label=f"Information sector (BLS JOLTS ≈{j['information']*12:.0f}%/yr)")
sp = stab[stab.month == "2025-09"].iloc[0]
ax.annotate(f"Sept 2025: {sp.quit_rate_ann_pct:.0f}%\n(deferred-resignation\nFY-end exodus)",
            xy=(sp.date, sp.quit_rate_ann_pct), xytext=(sp.date, 40),
            fontsize=9, ha="center", color=NAVY, arrowprops=dict(arrowstyle="->", color=NAVY))
ax.set_ylabel("Voluntary quit rate (annualized %)")
ax.set_title("The stability was real — until it wasn't\nFederal tech voluntary quit rate: ~2%/yr for years, a 27× spike in 2025, then reset",
             fontweight="bold", loc="left")
ax.legend(loc="upper left", fontsize=9, framealpha=.95); ax.set_ylim(0, 52)
plt.tight_layout(); plt.savefig("03_stability.png", bbox_inches="tight"); plt.close()

print("wrote 01_pay_gap.png, 02_seniority.png, 03_stability.png")
