"""Charts for the 'not a research role' analysis. Brand + dataviz-skill compliant."""
import json
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import brand as B

prev = pd.read_csv("prevalence_by_role.csv")
pay  = pd.read_csv("pay_effects.csv")
cm   = pd.read_csv("cooccurrence_llm_matched.csv")
F    = json.load(open("facts.json"))
PCT  = lambda v,_: f"{v:.0f}%"

# ---------------------------------------------------------------- 1. prevalence
anti = prev[prev.register=="anti_research_strict"].set_index("role_group")
rpos = prev[prev.register=="research_positive"].set_index("role_group")
order = anti["pct"].sort_values().index.tolist()
fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.6))
for ax, tab, col, ttl, xmax in [
        (axes[0], anti, B.VIOLET, 'Says the job is NOT research  (scale: 0 to 5%)', 5.0),
        (axes[1], rpos, B.CYAN,   'Names research, evals or experimentation as the job  (scale: 0 to 80%)', 82.0)]:
    y = np.arange(len(order)); v = tab.loc[order,"pct"].values
    ax.barh(y, v, height=0.62, color=col, zorder=3,
            error_kw=dict(ecolor=B.MUTE, lw=1.1, capsize=0))
    ax.errorbar(v, y, xerr=[v-tab.loc[order,"ci_lo"].values, tab.loc[order,"ci_hi"].values-v],
                fmt="none", ecolor=B.INK, lw=1.0, capsize=2.5, alpha=0.55, zorder=4)
    hi = tab.loc[order,"ci_hi"].values
    for yi, vi, hii in zip(y, v, hi):
        ax.text(hii + xmax*0.022, yi, f"{vi:.2f}%" if xmax < 10 else f"{vi:.0f}%",
                va="center", ha="left", fontsize=9, color=B.INK, weight="semibold", zorder=5)
    ax.set_yticks(y); ax.set_yticklabels(order, fontsize=9.5)
    ax.set_xlim(0, xmax); ax.set_title(ttl, fontsize=10.6, weight="semibold",
                                       color=B.INK, loc="left", pad=8)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:g}%"))
    B.tidy(ax)
axes[1].set_yticklabels([])
top, bot = B.layout(fig, header_in=1.06, footer_in=1.24)
B.header(fig, "Job ads that disclaim research are rare. Ads that demand it are everywhere.",
         "Share of US tech job postings using each register, within each role family. Bars show 95% Wilson intervals.\n"
         "The two panels use different scales, marked in each panel title.",
         y=top+0.152, dy=0.044)
B.footer(fig,
    f"Skillenai enriched job index, {F['postings']:,} US postings with full description text from {F['employers']:,} employers, snapshot September 2026.\n"
    "\"Not research\" counts ads that name research, papers, academia, researchers or notebooks in a subordinating construction:\n"
    "\"this is not a research role\", \"not just papers\", \"beyond the notebook\". Postings with empty descriptions are excluded.",
    y=bot-0.076)
B.stamp(fig, y=bot-0.086)
B.save_exact(fig, "01_who_disclaims_research.png")

# ---------------------------------------------------------------- 2. pay forest
LAB = {"f_evals":"Evaluation work (evals, eval harness,\noffline/model evaluation)",
       "f_phd":"PhD mentioned",
       "f_pipeline":"Research or prototype \"to production\"",
       "f_prod_grade":"Production-grade / production systems",
       "f_research_any":"Publications, venues, research culture",
       "f_experimentation":"Rigorous experimentation, ablations",
       "f_ship_register":"\"Ship fast\", \"bias for action\", \"move fast\"",
       "f_stats_rigor":"A/B testing, statistical methods",
       "f_strict":"\"This is not a research role\"",
       "f_placebo_eoe":"CALIBRATION: \"equal opportunity employer\""}
rows = pay[pay.register.isin(LAB)].copy()
rows["lab"] = rows.register.map(LAB)
main = rows[rows.register!="f_placebo_eoe"].sort_values("fe_pct")
plot = pd.concat([rows[rows.register=="f_placebo_eoe"], main])
y = np.arange(len(plot))
fig, ax = plt.subplots(figsize=(12.4, 7.7))
ax.axvline(0, color=B.INK, lw=1.0, alpha=0.5, zorder=2)
ax.axhline(0.5, color=B.GRID, lw=1.0, ls=(0,(4,3)), zorder=2)
ax.scatter(plot["naive_pct"], y, s=64, facecolor=B.BG, edgecolor=B.MUTE, lw=1.6,
           zorder=4, label="Raw gap between ads with and without the phrase")
ax.errorbar(plot["fe_pct"], y, xerr=[plot["fe_pct"]-plot["fe_lo"], plot["fe_hi"]-plot["fe_pct"]],
            fmt="o", ms=8, color=B.CYAN, ecolor=B.CYAN, elinewidth=2.0, capsize=3, zorder=5,
            label="Same employer, same level, same role family, same ad length")
for yi, r in zip(y, plot.itertuples()):
    ax.text(max(r.fe_hi, r.naive_pct) + 0.75, yi, f"{r.fe_pct:+.1f}%", va="center", ha="left", fontsize=8.8,
            color=B.INK if r.fe_p < 0.05 else B.MUTE,
            weight="semibold" if r.fe_p < 0.05 else "normal", zorder=6)
ax.set_yticks(y); ax.set_yticklabels(plot["lab"], fontsize=9.2)
ax.set_xlim(-11.5, 21.5)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:+.0f}%"))
ax.set_xlabel("Difference in advertised pay", fontsize=9.5, color=B.MUTE, labelpad=8)
B.tidy(ax)

top, bot = B.layout(fig, header_in=1.08, footer_in=1.66)
h, l = ax.get_legend_handles_labels()
fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, bot-0.004), ncol=2,
           fontsize=9, labelcolor=B.INK, handletextpad=0.6, columnspacing=2.4)
B.header(fig, "The swagger does not price. The evaluation work does.",
         "Advertised-pay difference for US tech postings that use each phrase. Hollow markers are the raw gap; filled markers hold\n"
         "employer, seniority, role family and ad length constant. Bars are 95% confidence intervals; bold labels are p < 0.05.",
         y=top+0.124, dy=0.036)
B.footer(fig,
    f"{F['salaried_n']:,} US salaried postings ({F['salaried_employers']:,} employers). The controlled model uses {F['fe_n']:,} postings at the {F['fe_employers']:,} employers posting 3 or more,\n"
    "comparing each ad with other ads at the same company. Pay units normalised; advertised base only, so equity is invisible.\n"
    "The calibration row is boilerplate that cannot plausibly change pay. Raw, it reads as a 9% pay cut, which is how much of every raw\n"
    "gap here is really a difference between companies. Holding employer constant it falls to 0.4%. That check is why the filled\n"
    "markers, and not the hollow ones, are the real prices.",
    y=bot-0.072)
B.stamp(fig, y=bot-0.082)
B.save_exact(fig, "02_what_the_words_are_worth.png")

# ---------------------------------------------------------------- 3. co-occurrence
cm = cm.set_index("role_group")
ordc = ["Software Engineer","ML Engineer","AI Engineer","Data Scientist"]
y = np.arange(len(ordc)); h = 0.34
fig, ax = plt.subplots(figsize=(12.6, 5.6))
ax.barh(y-h/2-0.012, cm.loc[ordc,"evals_in_anti"], height=h, color=B.VIOLET, zorder=3,
        label='Ads that say "this is not a research role"')
ax.barh(y+h/2+0.012, cm.loc[ordc,"evals_in_other"], height=h, color=B.CYAN, zorder=3,
        label="Every other ad in the same role")
for yi, g in zip(y, ordc):
    for off, col, sig in [(-h/2-0.012,"evals_in_anti",True), (h/2+0.012,"evals_in_other",False)]:
        v = cm.loc[g,col]
        ax.text(v+1.0, yi+off, f"{v:.1f}%", va="center", ha="left", fontsize=9,
                color=B.INK, weight="semibold" if sig else "normal", zorder=5)
    p = cm.loc[g,"p"]
    ax.text(95.0, yi+0.06, ("p < 0.001" if p < 0.001 else f"p = {p:.2f}"), va="center", ha="right",
            fontsize=8.6, color=B.INK if p < 0.05 else B.MUTE, zorder=5,
            weight="semibold" if p < 0.05 else "normal")
    ax.text(95.0, yi-0.20, f"n = {int(cm.loc[g,'n_anti_llm'])} vs {int(cm.loc[g,'n_other_llm']):,}",
            va="center", ha="right", fontsize=7.8, color=B.MUTE, zorder=5)
ax.set_yticks(y); ax.set_yticklabels(ordc, fontsize=10)
ax.set_xlim(0, 96); ax.set_xticks(range(0,71,10)); ax.invert_yaxis()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:g}%"))
ax.set_xlabel("Share of ads that ask for evaluation work", fontsize=9.5, color=B.MUTE, labelpad=8)
B.tidy(ax)

top, bot = B.layout(fig, header_in=1.02, footer_in=1.50)
h3, l3 = ax.get_legend_handles_labels()
fig.legend(h3, l3, loc="upper center", bbox_to_anchor=(0.5, bot-0.002), ncol=2,
           fontsize=9, labelcolor=B.INK, handletextpad=0.6, columnspacing=2.4)
B.header(fig, "The ads that disclaim research are asking for research anyway",
         "Among postings that mention LLMs or generative AI, the share that ask for evaluation work: eval harnesses, offline and\n"
         "model evaluation, LLM-as-a-judge. Like compared with like, so the gap is not just \"AI jobs versus everything else\".",
         y=top+0.158, dy=0.046)
B.footer(fig,
    f"{F['llm_matched_pooled']['anti_n']} postings carrying the disclaimer versus {F['llm_matched_pooled']['other_n']:,} that do not, all of them LLM or generative-AI postings. Two-proportion z-tests.\n"
    "The gap is large in software and ML engineering and absent inside AI Engineer, where evaluation is roughly 40% of ads\n"
    "whether or not they disclaim research. Read that null as the sharper result: within a role, the disclaimer tells a\n"
    "candidate nothing about whether the work involves evaluation.",
    y=bot-0.098)
B.stamp(fig, y=bot-0.108)
B.save_exact(fig, "03_asking_for_it_anyway.png")
print("done")
