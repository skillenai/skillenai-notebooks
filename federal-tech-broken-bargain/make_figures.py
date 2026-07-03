"""Figures for the federal-tech 'broken bargain' analysis (pay + mobility-vs-security + pension hinge)."""
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
inv = pd.read_csv("federal_involuntary.csv")
age = pd.read_csv("stability_by_age.csv")
B = json.load(open("private_and_bls.json"))
qn = B["bls_jolts_quits_rate_monthly_pct_may2026"]
ld = B["bls_jolts_layoffs_discharges_rate_monthly_pct_may2026"]

# ---------- FIG 1: Pay ----------
fig, ax = plt.subplots(figsize=(11, 6))
roles = ["Data Scientist", "Software Engineer"]
fed_map = {"Data Scientist": "Data Scientist", "Software Engineer": "Software Engineer / IT"}
y = np.arange(len(roles)); h = 0.36
for i, r in enumerate(roles):
    fp = pay[pay.role == fed_map[r]].iloc[0]; pv = B["private_posted_salary_us_usd"][r]
    ax.barh(y[i] + h/2, pv["max_p50"] - pv["min_p50"], left=pv["min_p50"], height=h, color=TEAL, alpha=.85,
            label="Private posted band (p50 min→max)" if i == 0 else "")
    ax.plot((pv["min_p50"]+pv["max_p50"])/2, y[i]+h/2, "o", color=NAVY, ms=7, label="Private midpoint" if i == 0 else "")
    ax.barh(y[i] - h/2, fp.incumbent_p75 - fp.incumbent_p25, left=fp.incumbent_p25, height=h, color=CORAL, alpha=.85,
            label="Federal incumbent band (p25→p75)" if i == 0 else "")
    ax.plot(fp.incumbent_p50, y[i]-h/2, "s", color=NAVY, ms=7, label="Federal incumbent median" if i == 0 else "")
ax.axvline(197200, color=GREY, ls="--", lw=1.5)
ax.text(199500, 0.5, "GS-15 ceiling\n(~$197K, locality-adj.)\nfederal base caps here;\nprivate has no ceiling",
        va="center", ha="left", fontsize=8.5, color="#4a4a4a")
ax.set_yticks(y); ax.set_yticklabels(roles); ax.xaxis.set_major_formatter(usd)
ax.set_xlabel("Annual base pay (USD)")
ax.set_title("The price of the bargain: a federal tech pay penalty\nFederal incumbent base (2026) vs private posted base — before equity or bonus",
             fontweight="bold", loc="left")
ax.legend(loc="lower right", fontsize=9, framealpha=.95); ax.set_xlim(80000, 260000)
plt.tight_layout(); plt.savefig("01_pay_gap.png", bbox_inches="tight"); plt.close()

# ---------- FIG 2: The bargain — mobility vs security ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.4))
groups = ["Federal tech", "Information\n(private tech)", "Total private"]
cols = [NAVY, TEAL, CORAL]
mob = [1.8, qn["information"]*12, qn["total_private"]*12]
a1.bar(groups, mob, color=cols)
for i, v in enumerate(mob): a1.text(i, v+0.6, f"{v:.0f}%", ha="center", fontweight="bold")
a1.set_title("MOBILITY\nVoluntary quit rate (annualized)", fontweight="bold", loc="left")
a1.set_ylabel("% per year"); a1.set_ylim(0, 30)
sec = [0.01, ld["information"]*12, ld["total_private"]*12]
a2.bar(groups, sec, color=cols)
for i, v in enumerate(sec):
    a2.text(i, v+0.6, ("≈0%" if v < 0.1 else f"{v:.0f}%"), ha="center", fontweight="bold")
a2.annotate("federal peak in the\n2025 exodus: 0.8%", xy=(0, 0.5), xytext=(0.15, 8),
            fontsize=8.5, color="#4a4a4a", arrowprops=dict(arrowstyle="->", color=GREY))
a2.set_title("SECURITY\nInvoluntary job-loss rate (annualized)", fontweight="bold", loc="left")
a2.set_ylabel("% per year"); a2.set_ylim(0, 30)
fig.suptitle("Two different things: federal tech workers rarely leave — and are almost never pushed out",
             fontweight="bold", x=0.01, ha="left", fontsize=13)
plt.tight_layout(); plt.savefig("02_bargain.png", bbox_inches="tight"); plt.close()

# ---------- FIG 3: The pension hinge — golden handcuffs ----------
fig, ax = plt.subplots(figsize=(12, 5.6))
age2 = age[age.headcount > 100].copy(); x = np.arange(len(age2))
ax2 = ax.twinx()
ax2.bar(x, age2.retirements, color=GOLD, alpha=.7, width=.7, label="Retirements (2024, count)")
ax.plot(x, age2.quit_rate_pct, color=NAVY, lw=2.5, marker="o", ms=6, label="Voluntary quit rate")
ax.set_zorder(ax2.get_zorder()+1); ax.patch.set_visible(False)
ax.set_xticks(x); ax.set_xticklabels(age2.age, rotation=0, fontsize=9)
ax.set_ylabel("Quit rate (%/yr)", color=NAVY); ax.set_ylim(0, 6.2)
ax2.set_ylabel("Retirements (count)", color="#b8860b")
ax.axvspan(7.5, 10.5, color=GOLD, alpha=.12)
ax.text(9, 5.6, "pension-eligibility\nages (55–65):\nexit wave", ha="center", fontsize=9, color="#8a6d00")
ax.set_title("The pension hinge: quits fall as the pension vests, then a retirement cliff at eligibility\n"
             "Federal tech, 2024 — the golden-handcuff signature", fontweight="bold", loc="left")
l1, la1 = ax.get_legend_handles_labels(); l2, la2 = ax2.get_legend_handles_labels()
ax.legend(l1+l2, la1+la2, loc="upper center", fontsize=9, framealpha=.95)
plt.tight_layout(); plt.savefig("03_pension_hinge.png", bbox_inches="tight"); plt.close()

# ---------- FIG 4: The 2025 twist — cut by buyouts, not layoffs ----------
fig, ax = plt.subplots(figsize=(12, 5.2))
inv["date"] = pd.to_datetime(inv.month + "-01")
ax.plot(inv.date, inv.quit_rate_tech_ann, color=NAVY, lw=2, marker="o", ms=3, label="Voluntary quits (mobility)")
ax.plot(inv.date, inv.rif_rate_tech_ann, color=CORAL, lw=2, marker="s", ms=3, label="Involuntary RIF (layoffs)")
sp = inv[inv.month == "2025-09"].iloc[0]
ax.annotate(f"Sept 2025: quits {sp.quit_rate_tech_ann:.0f}% vs RIF {sp.rif_rate_tech_ann:.1f}%\n"
            "the ~12% federal cut ran through\nvoluntary buyouts, not layoffs",
            xy=(sp.date, sp.quit_rate_tech_ann), xytext=(sp.date, 34), fontsize=9, ha="center", color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY))
ax.set_ylabel("Annualized rate (%)")
ax.set_title("The 2025 twist: the 'no layoffs' promise held in letter — the cut came through buyouts\n"
             "Federal tech voluntary quits vs involuntary RIF", fontweight="bold", loc="left")
ax.legend(loc="upper left", fontsize=9, framealpha=.95); ax.set_ylim(0, 52)
plt.tight_layout(); plt.savefig("04_twist.png", bbox_inches="tight"); plt.close()
print("wrote 01_pay_gap.png, 02_bargain.png, 03_pension_hinge.png, 04_twist.png")
