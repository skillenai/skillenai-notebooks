"""Charts for the remote-pay-geography analysis. Uses the shared Skillenai brand module."""
import json, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import brand as B

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
R = json.load(open(f"{OUT}/results.json"))

# Work-model ramp: ordered by degree of remoteness, monotone lightness (CVD-safe).
WM = {"onsite": "#2B2E8C", "hybrid": "#2E63C4", "remote": "#35A0D8"}

def head(fig, title, subtitle):
    """brand.header's dy is a FIGURE FRACTION; on short figures that collapses the
    title/subtitle gap. Convert to a fixed ~0.30in offset so it reads the same at any height."""
    B.header(fig, title, subtitle, dy=0.30 / fig.get_size_inches()[1])

SRC = ("Source: Skillenai labor-market index (prod-enriched-jobs). 46,873 US postings with a\n"
       "structured USD pay range, Mar-Sep 2026. Base-range midpoint; excludes equity and bonus.")

# ---------- FIG 1: the premium collapses under controls ----------
step = pd.DataFrame(R["stepwise"])
fig, ax = plt.subplots(figsize=(8.6, 5.4))
top, bot = B.layout(fig, header_in=1.16, footer_in=0.92)
fig.subplots_adjust(left=0.095, right=0.985)
xs = np.arange(len(step))
bars = ax.bar(xs, step["pct"], width=0.6, color=[WM["remote"]]*len(step))
bars[0].set_color(B.VIOLET)
ax.errorbar(xs, step["pct"], yerr=[step["pct"]-step["lo"], step["hi"]-step["pct"]],
            fmt="none", ecolor=B.INK, elinewidth=1.1, capsize=3, alpha=.55)
for i, v in enumerate(step["pct"]):
    ax.text(i, step["hi"].iloc[i] + 0.22, f"{v:+.1f}%", ha="center", va="bottom",
            fontsize=10, weight="bold", color=B.INK)
ax.axhline(0, color=B.INK, lw=1.0)
ax.set_xticks(xs)
ax.set_xticklabels([s.replace("+ ", "+\n").replace(" (", "\n(") for s in step["spec"]], fontsize=9)
ax.set_ylabel("Remote pay vs. onsite (%)", fontsize=9.5)
ax.set_ylim(-0.9, step["hi"].max() + 1.5)
B.tidy(ax, xgrid=False); ax.grid(axis="y", color=B.GRID, alpha=.75, lw=.7)
head(fig, "The remote pay premium is a composition artifact",
         "Same regression, one control added at a time. Once you compare like role with like role,\n"
         "the 7% raw premium is gone. Bars show 95% confidence intervals.")
B.footer(fig, SRC, y=bot-0.012); B.stamp(fig, x=0.905, y=bot-0.052, h=0.026)
B.save_exact(fig, f"{OUT}/01_premium_collapse.png")

# ---------- FIG 2 (COVER): geographic pass-through ----------
gt = pd.DataFrame(R["state_table"])
fig, ax = plt.subplots(figsize=(9.2, 7.6))
top, bot = B.layout(fig, header_in=1.22, footer_in=0.92)
fig.subplots_adjust(left=0.095, right=0.985)
lim = [min(gt.onsite_prem_pct.min(), gt.remote_prem_pct.min()) - 4,
       max(gt.onsite_prem_pct.max(), gt.remote_prem_pct.max()) + 4]
ax.plot(lim, lim, ls=(0, (5, 4)), color=B.MUTE, lw=1.3, zorder=1)
ax.text(lim[1]-0.6, lim[1]-3.2, "geography matters exactly\nas much when remote",
        ha="right", va="top", fontsize=8.6, color=B.MUTE, style="italic", linespacing=1.4)
is_md = gt.state.eq("Maryland")
ax.scatter(gt.onsite_prem_pct[~is_md], gt.remote_prem_pct[~is_md],
           s=np.sqrt(gt.n_onsite[~is_md] + gt.n_remote[~is_md]) * 4.2,
           color=B.CYAN, alpha=.85, edgecolor="white", lw=1.3, zorder=3)
ax.scatter(gt.onsite_prem_pct[is_md], gt.remote_prem_pct[is_md],
           s=np.sqrt(gt.n_onsite[is_md] + gt.n_remote[is_md]) * 4.2,
           facecolor="white", edgecolor=B.MUTE, lw=1.6, zorder=3)
pt = R["passthrough_noMD"]["remote"]
sub = gt[~is_md]
b = pt["slope"]; a = np.average(sub.remote_prem_pct) - b*np.average(sub.onsite_prem_pct)
ax.plot(np.array(lim), a + b*np.array(lim), color=B.VIOLET, lw=2.3, zorder=2,
        label=f"fitted pass-through = {b:.2f}  [{pt['lo']:.2f}, {pt['hi']:.2f}]")
for _, r in gt.iterrows():
    dy = -16 if r.state in ("New York", "Georgia") else 12
    ax.annotate(r.state if r.state != "District of Columbia" else "D.C.",
                (r.onsite_prem_pct, r.remote_prem_pct), textcoords="offset points",
                xytext=(0, dy), ha="center", fontsize=8.4,
                color=B.MUTE if r.state == "Maryland" else B.INK)
ax.annotate("Maryland: cleared defense work,\nonsite by necessity (excluded from fit)",
            (gt.onsite_prem_pct[is_md].iloc[0], gt.remote_prem_pct[is_md].iloc[0]),
            textcoords="offset points", xytext=(-12, -34), ha="right", fontsize=8,
            color=B.MUTE, style="italic", linespacing=1.4,
            arrowprops=dict(arrowstyle="-", color=B.MUTE, lw=.8, alpha=.7))
ax.set_xlim(lim); ax.set_ylim(lim)
ax.axhline(0, color=B.GRID, lw=.9); ax.axvline(0, color=B.GRID, lw=.9)
ax.set_xlabel("Onsite pay premium for this state (%)", fontsize=9.5)
ax.set_ylabel("Remote pay premium for this state (%)", fontsize=9.5)
ax.legend(loc="lower right", fontsize=9)
B.tidy(ax, xgrid=False, spines=("top","right"))
ax.grid(color=B.GRID, alpha=.6, lw=.7)
head(fig, "Remote work did not create a national pay scale",
         "Each bubble is a state. If remote pay ignored location, the dots would flatten onto a\n"
         "horizontal line. They sit on the diagonal instead. Pay residualized on role and level.")
B.footer(fig, SRC, y=bot-0.012); B.stamp(fig, x=0.905, y=bot-0.052, h=0.026)
B.save_exact(fig, f"{OUT}/02_geographic_passthrough.png")

# ---------- FIG 3: the platforms disagree ----------
rob = pd.DataFrame(R["platform_robustness"]).sort_values("pct")
fig, ax = plt.subplots(figsize=(8.8, 4.9))
top, bot = B.layout(fig, header_in=1.16, footer_in=0.92)
fig.subplots_adjust(left=0.155, right=0.985)
ys = np.arange(len(rob))
ax.errorbar(rob["pct"], ys, xerr=[rob["pct"]-rob["lo"], rob["hi"]-rob["pct"]],
            fmt="o", color=B.VIOLET, ecolor=B.VIOLET, elinewidth=2, capsize=4, markersize=8)
pooled = R["full"]["remote"]["pct"]
ax.axvline(pooled, color=B.CYAN, lw=1.8, ls=(0,(4,3)), zorder=1,
           label=f"pooled estimate {pooled:+.1f}%")
ax.axvline(0, color=B.INK, lw=1.0)
for i, r in enumerate(rob.itertuples()):
    ax.text(r.hi + 0.3, i, f"{r.pct:+.1f}%  (n={r.n:,})", va="center", fontsize=8.8, color=B.INK)
ax.set_yticks(ys); ax.set_yticklabels(rob["platform"], fontsize=9.5)
ax.set_xlabel("Remote pay vs. onsite, same role and level (%)", fontsize=9.5)
ax.set_xlim(rob["lo"].min()-1.2, rob["hi"].max()+3.4)
ax.legend(loc="lower right", fontsize=8.8)
B.tidy(ax)
head(fig, "Why we will not print a single number for the remote gap",
         "Three job-board sources, same model, three incompatible answers. The pooled estimate\n"
         "averages a penalty and a premium, so we report the disagreement instead.")
B.footer(fig, SRC, y=bot-0.012); B.stamp(fig, x=0.905, y=bot-0.052, h=0.026)
B.save_exact(fig, f"{OUT}/03_platform_disagreement.png")

# ---------- FIG 4: level mix + pay by level ----------
mix = pd.DataFrame(R["level_mix"])
order = [l for l in ["Entry","Mid","Senior","Staff+","Management","Exec"] if l in mix.columns]
mix = mix.loc[["onsite","hybrid","remote"], order]
lv = pd.DataFrame(R["by_level"]); lvn = pd.DataFrame(R["by_level_n"])
ic = [l for l in ["Entry","Mid","Senior","Staff+"] if l in lv.index]

fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.6))
top, bot = B.layout(fig, header_in=1.20, footer_in=1.85)
fig.subplots_adjust(left=0.075, right=0.985, wspace=0.22)
ax = axes[0]
left = np.zeros(len(mix))
ramp = [B.RUNG[0], B.RUNG[1], B.RUNG[2], B.RUNG[3], B.MUTE, "#C9CFDC"]
for j, c in enumerate(order):
    ax.barh(mix.index, mix[c], left=left, color=ramp[j], height=.62,
            label=c, edgecolor=B.BG, lw=.8)
    for i, v in enumerate(mix[c]):
        if v > 6:
            ax.text(left[i]+v/2, i, f"{v:.0f}", ha="center", va="center",
                    fontsize=8.4, color="white", weight="bold")
    left += mix[c].values
ax.set_xlim(0, 100); ax.set_xlabel("Share of postings (%)", fontsize=9.5)
ax.set_title("Remote postings skew senior", fontsize=10.5, weight="bold", color=B.INK, loc="left")
ax.legend(fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(.5, -.155))
B.tidy(ax)

ax = axes[1]
x = np.arange(len(ic)); w = .26
for i, wm in enumerate(["onsite","hybrid","remote"]):
    ax.bar(x + (i-1)*w, [lv.loc[l, wm] for l in ic], w, color=WM[wm], label=wm)
ax.set_xticks(x); ax.set_xticklabels(ic, fontsize=9.5)
ax.yaxis.set_major_formatter(B.K)
ax.set_title("but within a rung, the gap nearly closes", fontsize=10.5,
             weight="bold", color=B.INK, loc="left")
ax.legend(fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(.5, -.155))
B.tidy(ax, xgrid=False); ax.grid(axis="y", color=B.GRID, alpha=.75, lw=.7)
head(fig, "Where the raw premium actually comes from",
         "Remote roles are disproportionately senior. That mix, not the work model, is what lifts\n"
         "the headline remote median above onsite.")
B.footer(fig, SRC, y=0.075); B.stamp(fig, x=0.905, y=0.028, h=0.026)
B.save_exact(fig, f"{OUT}/04_level_mix_and_pay.png")
print("charts done")

# ---------- FIG 5: employer vs location, person-scale (new cover) ----------
dec = R["decomposition"]; sp = R["offer_spread"]
pt = pd.DataFrame(R["predicted_by_state"])
fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.2), gridspec_kw={"width_ratios": [1.25, 1]})
top, bot = B.layout(fig, header_in=1.24, footer_in=1.05)
fig.subplots_adjust(left=0.115, right=0.985, wspace=0.34)

ax = axes[0]
pt2 = pt.sort_values("predicted")
cols = [B.CYAN if v >= pt2.predicted.median() else "#9AD9E8" for v in pt2.predicted]
ax.barh(pt2.state, pt2.predicted, color=cols, height=.66)
for i, r in enumerate(pt2.itertuples()):
    ax.text(r.predicted - 2600, i, f"${r.predicted/1000:.0f}K", va="center", ha="right",
            fontsize=8.8, color="white", weight="bold")
ax.set_xlim(0, pt2.predicted.max() * 1.06)
ax.xaxis.set_major_formatter(B.K)
ax.set_title(f"Same job, \${sp['spread_usd']/1000:.0f}K apart", fontsize=10.5,
             weight="bold", color=B.INK, loc="left")
ax.set_xlabel("Predicted pay, remote senior software engineer", fontsize=9)
B.tidy(ax)

ax = axes[1]
labels = ["Which state\nthe posting names", "Which employer\nis hiring"]
vals = [dec["unique_state_adj"], dec["unique_company_adj"]]
bars = ax.bar([0, 1], vals, color=[B.MUTE, B.VIOLET], width=.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.008, f"{v:+.3f}", ha="center", fontsize=11, weight="bold", color=B.INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(labels, fontsize=9.2)
ax.set_ylabel("Unique variance explained (adjusted R²)", fontsize=9)
ax.set_ylim(0, max(vals) * 1.22)
ax.set_title(f"Employer explains {dec['ratio']:.0f}x more", fontsize=10.5,
             weight="bold", color=B.INK, loc="left")
ax.annotate("a placebo with the same\nnumber of fake employers\nexplains nothing (+0.000)",
            xy=(1, dec["unique_company_adj"]), xytext=(-0.44, max(vals)*0.72),
            fontsize=8.2, color=B.MUTE, style="italic", linespacing=1.4)
B.tidy(ax, xgrid=False); ax.grid(axis="y", color=B.GRID, alpha=.75, lw=.7)

head(fig, "Your remote salary is set by who hires you, not where you sit",
     "Left: what the same remote senior software engineer role pays, by the state the employer is\n"
     "anchored in. Right: how much each factor explains once the other is already known.")
B.footer(fig, SRC, y=0.055); B.stamp(fig, x=0.905, y=0.012, h=0.026)
B.save_exact(fig, f"{OUT}/05_employer_vs_location.png")
print("fig 5 done")
