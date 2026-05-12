#!/usr/bin/env python3
"""Figures for the LLM-eval-landscape analysis.

All counts are phrase-prevalence (`match_phrase` on `extractedText`) over the
Skillenai enriched indices, gathered 2026-05-12. See README.md for methodology.
Re-runnable without the API: the numbers below are the captured query results.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"figure.dpi": 150, "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# --- corpus totals (docs) ---
TOT = {"jobs": 156928, "blog": 349305, "news": 86184, "scholarly": 31720}
AI_JOBS = 33580            # job posts mentioning an LLM/GenAI term
AI_EVAL_JOBS = 8569        # job posts mentioning an LLM/GenAI term AND an eval/benchmark term

C_JOBS = "#1f6feb"
C_MEDIA = "#d29922"
C_SCHOL = "#8957e5"

# ============================================================
# Fig 1 — eval-tool "market share" (share of all dedicated-eval-tool mentions)
# ============================================================
# (jobs_count, blog_count, news_count); Arize folds in the "arize phoenix" phrase
TOOLS = {
    "LangSmith":            (317, 500, 67),
    "Langfuse":             (256, 289, 20),
    "Arize / Phoenix":      (97,  347, 43),
    "Braintrust*":          (100, 138, 25),
    "RAGAS":                (93,  167, 19),
    "DeepEval":             (58,  129, 16),
    "promptfoo":            (26,  128, 124),
    "Helicone":             (11,  78,  12),
    "PromptLayer":          (6,   118, 14),
    "Confident AI":         (2,   87,  10),
    "Galileo":              (6,   74,  8),
    "Pydantic Logfire":     (12,  40,  2),
    "Comet Opik":           (1,   48,  5),
    "Traceloop/OpenLLMetry":(0,   47,  9),
    "Evidently AI":         (0,   54,  6),
    "WhyLabs / LangKit":    (3,   49,  3),
    "Fiddler AI":           (17,  21,  2),
    "TruLens":              (7,   32,  6),
    "Humanloop":            (0,   32,  13),
    "Langtrace":            (6,   1,   0),
    "DeepChecks":           (1,   29,  2),
    "Giskard":              (1,   18,  5),
    "Vellum":               (2,   18,  7),
    "Maxim AI":             (0,   22,  7),
    "LangWatch":            (0,   10,  4),
    "Patronus AI":          (0,   6,   5),
    "HoneyHive":            (2,   6,   1),
}
jobs_total = sum(v[0] for v in TOOLS.values())
media_total = sum(v[1] + v[2] for v in TOOLS.values())
rows = sorted(TOOLS.items(), key=lambda kv: -(kv[1][0] / jobs_total + (kv[1][1] + kv[1][2]) / media_total))
names = [r[0] for r in rows]
job_share = [r[1][0] / jobs_total * 100 for r in rows]
media_share = [(r[1][1] + r[1][2]) / media_total * 100 for r in rows]

fig, ax = plt.subplots(figsize=(11, 8))
y = np.arange(len(names))[::-1]
h = 0.4
ax.barh(y + h/2, job_share, height=h, color=C_JOBS, label=f"Job postings (n={jobs_total:,} tool mentions)")
ax.barh(y - h/2, media_share, height=h, color=C_MEDIA, label=f"Blogs + news (n={media_total:,} tool mentions)")
for yi, js, ms, (nm, (jc, bc, nc)) in zip(y, job_share, media_share, rows):
    ax.text(js + 0.4, yi + h/2, f"{js:.0f}%  ({jc})", va="center", fontsize=8)
    ax.text(ms + 0.4, yi - h/2, f"{ms:.0f}%  ({bc+nc})", va="center", fontsize=8, color="#6e4f00")
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlabel("Share of all dedicated-eval-tool mentions in the corpus (%)")
ax.set_title("The LLM-eval tool 'market': who employers name vs who the press names\n"
             "Skillenai enriched indices, May 2026 — phrase prevalence in posting / article text", fontsize=12)
ax.legend(loc="lower right", frameon=False)
ax.set_xlim(0, max(max(job_share), max(media_share)) * 1.18)
fig.text(0.01, 0.01, "*Braintrust: ~80% of job mentions co-occur with an LLM/eval/LangChain context; treat as approximate.",
         fontsize=7.5, color="#666")
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("01_tool_market_share.png", bbox_inches="tight")
plt.close(fig)

# ============================================================
# Fig 2 — the three worlds: jobs-rate vs blog-rate, log-log, colored by category
# ============================================================
# (jobs_count, blog_count, category) ; rate per 10k docs of that corpus
ITEMS = {
    # production tools
    "LangSmith": (317, 500, "Production tool"),
    "Langfuse": (256, 289, "Production tool"),
    "RAGAS": (93, 167, "Production tool"),
    "DeepEval": (58, 129, "Production tool"),
    "Arize/Phoenix": (97, 347, "Production tool"),
    "promptfoo": (26, 128, "Production tool"),
    # methodology
    "LLM-as-a-judge": (183, 709, "Methodology"),
    "rubric scoring": (120, 1346, "Methodology"),
    "online eval": (134, 118, "Methodology"),
    "offline eval": (135, 158, "Methodology"),
    "evals in CI": (59, 436, "Methodology"),
    "eval pipeline/harness": (338, 1245, "Methodology"),
    "agentic eval": (123, 328, "Methodology"),
    "red teaming": (638, 2030, "Methodology"),
    "hallucination detection": (78, 717, "Methodology"),
    "eval-driven development": (19, 72, "Methodology"),
    "calibration": (47, 389, "Methodology"),
    "inter-rater agreement": (33, 138, "Methodology"),
    # academic metrics / agreement stats
    "BLEU/ROUGE/BERTScore": (27, 740, "Academic metric"),
    "G-Eval": (3, 77, "Academic metric"),
    "pass@k": (37, 387, "Academic metric"),
    "Cohen's kappa": (1, 23, "Academic metric"),
    "Elo / arena rating": (1, 162, "Academic metric"),
    # capability benchmarks
    "SWE-bench": (23, 1474, "Capability benchmark"),
    "MMLU": (14, 654, "Capability benchmark"),
    "GPQA": (4, 543, "Capability benchmark"),
    "HumanEval": (5, 420, "Capability benchmark"),
    "ARC-AGI": (8, 384, "Capability benchmark"),
    "Chatbot Arena": (11, 323, "Capability benchmark"),
    "LiveCodeBench": (1, 293, "Capability benchmark"),
    "model/system card": (11, 889, "Capability benchmark"),
}
CAT_COLORS = {
    "Production tool": "#1f6feb",
    "Methodology": "#2da44e",
    "Academic metric": "#8957e5",
    "Capability benchmark": "#cf222e",
}
fig, ax = plt.subplots(figsize=(11, 8.5))
for nm, (jc, bc, cat) in ITEMS.items():
    jr = max(jc, 0.5) / TOT["jobs"] * 10000
    br = max(bc, 0.5) / TOT["blog"] * 10000
    ax.scatter(jr, br, s=70, color=CAT_COLORS[cat], edgecolor="white", linewidth=0.7, zorder=3)
    ax.annotate(nm, (jr, br), xytext=(5, 3), textcoords="offset points", fontsize=8.2)
lim = [0.04, 120]
ax.plot(lim, lim, ":", color="#999", zorder=1, label="equal rate (jobs = blogs)")
ax.fill_between(lim, lim, [l*400 for l in lim], color="#cf222e", alpha=0.05, zorder=0)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.045, 60); ax.set_ylim(0.4, 130)
ax.set_xlabel("Prevalence in job postings  (mentions per 10,000 posts)")
ax.set_ylabel("Prevalence in blog posts  (mentions per 10,000 posts)")
ax.set_title("Three worlds of LLM evaluation: hiring, practitioner discourse, and the leaderboard race\n"
             "Above the dotted line = talked about far more than hired for", fontsize=12)
handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=10, label=k) for k, c in CAT_COLORS.items()]
handles.append(plt.Line2D([0], [0], ls=":", color="#999", label="equal rate"))
ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9)
fig.tight_layout()
fig.savefig("02_three_worlds.png", bbox_inches="tight")
plt.close(fig)

# ============================================================
# Fig 3 — practitioner vs researcher: which terms skew industry vs academia (log ratio of per-capita rates)
# ============================================================
import math
METH = {  # name: (jobs_count, scholarly_count)
    "online evaluation":                 (134, 13),
    "offline evaluation":                (135, 14),
    "evals wired into CI / CD":          (59, 8),
    "eval-driven development":           (19, 1),    # ~0 in papers; floored at 1
    "eval pipeline / harness / framework":(338, 467),
    "agentic / tool-use evaluation":     (153, 70),
    "LLM observability / tracing":       (107, 1),
    "hallucination detection":           (78, 76),
    "rubric-based scoring":              (120, 159),
    "LLM-as-a-judge":                    (183, 231),
    "synthetic eval data":               (9, 41),
    "preference data / win rate":        (110, 120),
    "inter-annotator agreement":         (33, 62),
    "answer relevancy / correctness":    (9, 113),
    "calibration (model / confidence)":  (47, 144),
    "G-Eval / GPTScore":                 (3, 7),
    "BLEU / ROUGE / BERTScore":          (27, 125),
    "pass@k / execution accuracy":       (37, 197),
    "Elo / Bradley-Terry / arena rating":(1, 28),
    "Cohen's / Fleiss' / Krippendorff' κ":(1, 42),
    "expected calibration error (ECE)":  (1, 22),
}
def logratio(jc, sc):
    jr = max(jc, 0.5) / TOT["jobs"]
    sr = max(sc, 0.5) / TOT["scholarly"]
    return math.log10(jr / sr)
rows = sorted(METH.items(), key=lambda kv: logratio(*kv[1]))
names = [r[0] for r in rows]
vals = [logratio(*r[1]) for r in rows]
fig, ax = plt.subplots(figsize=(11, 8))
y = np.arange(len(names))
colors = [C_JOBS if v >= 0 else C_SCHOL for v in vals]
bars = ax.barh(y, vals, color=colors, height=0.62)
for yi, v, (nm, (jc, sc)) in zip(y, vals, rows):
    ha = "left" if v >= 0 else "right"
    dx = 0.04 if v >= 0 else -0.04
    ax.text(v + dx, yi, f"{jc:g} jobs / {sc:g} papers", va="center", ha=ha, fontsize=7.8, color="#444")
ax.axvline(0, color="#333", lw=1)
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlabel("log₁₀( prevalence-per-doc in job postings  ÷  prevalence-per-doc in scholarly papers )")
ax.set_title("Two cultures of LLM evaluation: industry vocabulary vs research vocabulary\n"
             "Right (blue) = appears disproportionately in job postings   —   Left (purple) = disproportionately in research papers", fontsize=12)
ax.text(0.98, 0.04, "0 = referenced equally often per document in both corpora", transform=ax.transAxes,
        ha="right", fontsize=8, color="#666")
xmax = max(abs(min(vals)), abs(max(vals))) * 1.35
ax.set_xlim(-xmax, xmax)
fig.tight_layout()
fig.savefig("03_two_cultures.png", bbox_inches="tight")
plt.close(fig)

# ============================================================
# Fig 4 — who's expected to do LLM evals: by role (within AI-relevant postings)
# ============================================================
ROLES = {  # role: (N, named_platform_pct, llm_judge_pct, eval_word_pct)
    "AI Engineer":                 (1400, 6.29, 2.36, 58.1),
    "ML Engineer":                 (1662, 2.83, 0.96, 45.3),
    "Forward-deployed / Solutions":(649,  2.62, 0.00, 31.9),
    "Data / ML Platform & MLOps":  (824,  2.18, 0.12, 13.5),
    "Software Engineer (generic)": (6094, 1.84, 0.23, 22.4),
    "Data Scientist":              (896,  1.34, 2.12, 36.3),
    "Product Manager":             (1345, 0.67, 0.22, 24.7),
    "Research Scientist / Eng.":   (757,  0.53, 1.85, 51.8),
}
rows = sorted(ROLES.items(), key=lambda kv: kv[1][1])
names = [f"{r[0]}\n(n={r[1][0]:,})" for r in rows]
plat = [r[1][1] for r in rows]
judge = [r[1][2] for r in rows]
fig, ax = plt.subplots(figsize=(10.5, 7))
y = np.arange(len(names))
h = 0.38
b1 = ax.barh(y + h/2, plat, height=h, color=C_JOBS, label="Names a specific eval platform (LangSmith, Langfuse, RAGAS, …)")
b2 = ax.barh(y - h/2, judge, height=h, color="#2da44e", label="Names 'LLM-as-a-judge'")
ax.bar_label(b1, fmt="%.1f%%", padding=3, fontsize=8)
ax.bar_label(b2, fmt="%.1f%%", padding=3, fontsize=8)
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlabel("Share of that role's AI-relevant job postings (%)")
ax.set_title("Who's expected to do LLM evals?\nShare of AI-relevant postings per role that name a specific eval tool or the LLM-as-a-judge method", fontsize=12)
ax.legend(loc="lower right", frameon=False, fontsize=9)
ax.set_xlim(0, max(plat) * 1.25)
fig.tight_layout()
fig.savefig("04_eval_by_role.png", bbox_inches="tight")
plt.close(fig)

# ============================================================
# Fig 5 — the benchmark discourse gap (blog/news vs jobs, log x)
# ============================================================
BENCH = {  # name: (jobs, blog, news)
    "SWE-bench":              (23, 1474, 538),
    "MMLU / MMLU-Pro":        (14, 854, 234),
    "GPQA":                   (4, 543, 220),
    "HumanEval":              (5, 420, 70),
    "ARC-AGI":                (8, 384, 141),
    "Chatbot Arena / LMSYS":  (11, 323, 101),
    "LiveCodeBench":          (1, 293, 82),
    "GSM8K":                  (5, 196, 51),
    "AIME (math benchmark)":  (0, 152, 57),
    "FrontierMath":           (0, 139, 61),
    "Humanity's Last Exam":   (0, 88, 44),
    "HellaSwag":              (0, 75, 7),
    "tau-bench":              (4, 82, 25),
    "MT-Bench":               (0, 45, 14),
}
rows = sorted(BENCH.items(), key=lambda kv: kv[1][1] + kv[1][2])
names = [r[0] for r in rows]
jc = [r[1][0] for r in rows]
mc = [r[1][1] + r[1][2] for r in rows]
fig, ax = plt.subplots(figsize=(10.5, 7.5))
y = np.arange(len(names))
h = 0.4
ax.barh(y + h/2, [max(v, 0.6) for v in mc], height=h, color=C_MEDIA, label="Mentions across blogs + news")
ax.barh(y - h/2, [max(v, 0.6) for v in jc], height=h, color=C_JOBS, label="Mentions across 156,928 job postings")
for yi, j, m in zip(y, jc, mc):
    ax.text(max(m, 0.6) * 1.05, yi + h/2, f"{m:,}", va="center", fontsize=8, color="#6e4f00")
    ax.text(max(j, 0.6) * 1.05, yi - h/2, f"{j}", va="center", fontsize=8, color=C_JOBS)
ax.set_xscale("log")
ax.set_yticks(y); ax.set_yticklabels(names)
ax.set_xlabel("Document mentions (log scale)")
ax.set_title("The benchmarks everyone writes about — and nobody hires for\n"
             "Capability benchmarks dominate AI media coverage but are essentially absent from job postings", fontsize=12)
ax.legend(loc="lower right", frameon=False)
ax.set_xlim(0.5, max(mc) * 3)
fig.tight_layout()
fig.savefig("05_benchmark_gap.png", bbox_inches="tight")
plt.close(fig)

print("wrote 01_tool_market_share.png 02_three_worlds.png 03_two_cultures.png 04_eval_by_role.png 05_benchmark_gap.png")
