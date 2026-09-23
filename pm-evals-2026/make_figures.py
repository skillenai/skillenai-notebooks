"""Figures for pm-evals-2026. Reads the result CSVs in this folder."""
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from brand import CYAN, VIOLET, INK, MUTE, GRID, BG, header, footer, stamp, tidy, layout, save_exact

ORDER = ["AI Engineer", "ML Engineer", "Product Manager", "Data Scientist", "Software Engineer"]
SRC = "Source: Skillenai analysis of US job postings, Mar-Sep 2026 (n=63,316 with full text)."
pct = lambda v: f"{v:.1f}%"

def bold_pm(ax):
    for t in ax.get_yticklabels():
        if t.get_text() == "Product Manager":
            t.set_fontweight("bold")

# 1. rates by role
r = pd.read_csv("01_rates_by_role.csv").set_index("fam").loc[ORDER[::-1]]
fig, ax = plt.subplots(figsize=(10, 5.4))
y = np.arange(len(r)); h = 0.36
for off, col, c, lab in [(h / 2, "asked_pct", CYAN, "All postings in the role"),
                         (-h / 2, "asked_within_genai_pct", VIOLET, "Postings that also ask for GenAI skills")]:
    ax.barh(y + off, r[col], height=h - 0.04, color=c, label=lab)
    for yi, v in zip(y + off, r[col]):
        ax.text(v + 0.4, yi, pct(v), va="center", fontsize=9, color=INK)
ax.set_yticks(y, r.index); bold_pm(ax); tidy(ax)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%"); ax.set_xlim(0, 29)
ax.legend(loc="lower right", fontsize=9)
top, bot = layout(fig, header_in=0.85, footer_in=0.7)
header(fig, "PMs are asked for AI evals as often as data scientists",
       "Share of US job postings asking for AI/LLM evals, by role. Among GenAI postings, 1 in 7 PM roles asks.", y=0.985, dy=0.36 / fig.get_size_inches()[1])
footer(fig, SRC + "\nAI evals = eval skill extracted from the posting or eval language in its text, LLM-verified.", y=bot - 0.03)
stamp(fig, y=bot - 0.075); save_exact(fig, "01_rates_by_role.png")

# 2. spring vs late summer, same employers
t = pd.read_csv("02_trend.csv").set_index("fam").loc[ORDER[::-1]]
fig, ax = plt.subplots(figsize=(10, 5.0))
y = np.arange(len(t))
for yi, a, b in zip(y, t.stable_aprmay, t.stable_augsep):
    ax.plot([a, b], [yi, yi], color=GRID, lw=3, zorder=1, solid_capstyle="round")
ax.scatter(t.stable_aprmay, y, s=90, color=CYAN, zorder=3, label="Apr-May 2026", edgecolor=BG, linewidth=2)
ax.scatter(t.stable_augsep, y, s=90, color=VIOLET, zorder=3, label="Aug-Sep 2026", edgecolor=BG, linewidth=2)
for yi, (f, a, b) in zip(y, t[["stable_aprmay", "stable_augsep"]].itertuples()):
    ax.text(max(a, b) + 0.7, yi, f"{a:.1f}% to {b:.1f}%  ({b / a:.1f}x)", va="center", fontsize=9, color=INK)
ax.set_yticks(y, t.index); bold_pm(ax); tidy(ax)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%"); ax.set_xlim(0, 33)
ax.legend(loc="lower right", fontsize=9)
top, bot = layout(fig, header_in=0.85, footer_in=0.7)
header(fig, "The PM ask for AI evals doubled in four months",
       "Share of postings asking for AI evals, same employers in both periods. Data scientists were flat.", y=0.985, dy=0.36 / fig.get_size_inches()[1])
footer(fig, SRC + "\nEmployers posting in both Apr-May and Aug-Sep. Month = first seen. Trend adjusted for job board: PM p<0.0001.", y=bot - 0.03)
stamp(fig, y=bot - 0.075); save_exact(fig, "02_pm_doubled.png")

# 3. profiles vs postings
p = pd.read_csv("03_profiles_vs_postings.csv").set_index("fam").loc[ORDER[::-1]]
fig, ax = plt.subplots(figsize=(10, 5.0))
y = np.arange(len(p))
for yi, a, b in zip(y, p.profile_pct, p.postings_sep2026_pct):
    ax.plot([a, b], [yi, yi], color=GRID, lw=3, zorder=1, solid_capstyle="round")
ax.scatter(p.profile_pct, y, s=90, color=CYAN, zorder=3, label="Career profiles: positions started 2023-2025", edgecolor=BG, linewidth=2)
ax.scatter(p.postings_sep2026_pct, y, s=90, color=VIOLET, zorder=3, label="Job postings: September 2026", edgecolor=BG, linewidth=2)
for yi, (f, a, b, k, n) in zip(y, p[["profile_pct", "postings_sep2026_pct", "profile_eval", "profile_positions_2023_25"]].itertuples()):
    ax.text(b + 0.7, yi, f"{a:.1f}% of profiles ({k:,} of {n:,})  vs  {b:.1f}% of postings", va="center", fontsize=9, color=INK)
ax.set_yticks(y, p.index); bold_pm(ax); tidy(ax)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%"); ax.set_xlim(0, 42)
ax.legend(loc="lower right", fontsize=9)
top, bot = layout(fig, header_in=0.85, footer_in=0.7)
header(fig, "Employers ask for evals. Almost no PM lists them.",
       "AI-eval skill on career profiles (through ~Oct 2025) vs share of postings asking for AI evals (Sep 2026).", y=0.985, dy=0.36 / fig.get_size_inches()[1])
footer(fig, "Source: Skillenai career-profile graph (641K positions with extracted skills) and US job postings.\n"
       "Profiles are a stock of everyone in the role, postings are a flow of open roles: read the gap as direction, not an exact ratio.", y=bot - 0.03)
stamp(fig, y=bot - 0.075); save_exact(fig, "03_profiles_vs_postings.png")

# 4. responsibilities heatmap
s = pd.read_csv("04_responsibilities_sonnet.csv").set_index("fam").loc[ORDER]
ROWS = [("decide_ship", "Make ship / model decisions from results"),
        ("define_quality", "Define the quality bar and metrics*"),
        ("write_evals", "Write evals (cases, rubrics, LLM judges)"),
        ("run_monitor", "Run evals and monitor production"),
        ("infrastructure", "Build eval harnesses and pipelines"),
        ("datasets", "Build golden / eval datasets"),
        ("error_analysis", "Error analysis: review outputs, find failure modes"),
        ("safety", "Safety, hallucination and bias evals")]
M = s[[k for k, _ in ROWS]].T.values
cmap = LinearSegmentedColormap.from_list("seq", ["#EEF8FB", "#9AD9E8", "#35A0D8", "#2E63C4", "#2B2E8C"])
fig, ax = plt.subplots(figsize=(11, 6.2))
ax.imshow(M, cmap=cmap, vmin=0, vmax=80, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        ax.text(j, i, f"{v:.0f}%", ha="center", va="center", fontsize=10,
                color="white" if v >= 45 else INK, weight="bold" if ORDER[j] == "Product Manager" else "normal")
ax.set_xticks(range(len(ORDER)), [f"{f}\n(n={int(s.loc[f, 'n']):,})" for f in ORDER], fontsize=9)
ax.set_yticks(range(len(ROWS)), [l for _, l in ROWS], fontsize=9.5)
for t_ in ax.get_xticklabels():
    if t_.get_text().startswith("Product Manager"):
        t_.set_fontweight("bold")
ax.xaxis.tick_top(); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks(np.arange(-.5, len(ORDER)), minor=True); ax.set_yticks(np.arange(-.5, len(ROWS)), minor=True)
ax.grid(which="minor", color=BG, lw=2); ax.tick_params(which="minor", length=0)
top, bot = layout(fig, header_in=0.85, footer_in=0.8)
header(fig, "Error analysis goes to data scientists, not PMs",
       "Share of each role's eval-asking postings that assign each responsibility (a posting can assign several).", y=0.985, dy=0.36 / fig.get_size_inches()[1])
footer(fig, SRC + "\nResponsibilities labeled by Claude Sonnet 5; a second labeler (Haiku 4.5) agrees on the direction of every PM-vs-technical-roles difference.\n"
       "*The two labelers disagree on the level of 'define the quality bar' (kappa 0.37); treat that row as indicative.", y=bot - 0.02)
stamp(fig, y=bot - 0.085); save_exact(fig, "04_responsibilities.png")
