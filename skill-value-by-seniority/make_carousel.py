"""Build a LinkedIn PDF carousel from the skill-value-by-seniority analysis.

LinkedIn auto-renders uploaded PDFs as swipeable carousels. Optimal aspect is
4:5 portrait (1080x1350) for mobile feed. Each page = one slide.

Output: linkedin-carousel.pdf
"""
import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patheffects as pe
import numpy as np

# Disable matplotlib's mathtext parsing so $...$ doesn't render as LaTeX italic math
matplotlib.rcParams["text.parse_math"] = False

# LinkedIn portrait carousel: 1080x1350 px at 150 DPI = 7.2 x 9.0 inches
WIDTH, HEIGHT = 7.2, 9.0
DPI = 150

# Brand palette
GREEN = "#2E7D32"
GREEN_LIGHT = "#81C784"
YELLOW = "#F9A825"
RED = "#C62828"
RED_LIGHT = "#EF5350"
NAVY = "#102A43"
BG = "#FAFAF7"
INK = "#1A1A1A"
GREY = "#667"


def new_slide():
    fig = plt.figure(figsize=(WIDTH, HEIGHT), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def footer(ax, slide_num, total):
    ax.text(50, 3, "skillenai.com  ·  Skillenai Job Index",
            ha="center", va="center", fontsize=8, color=GREY, style="italic")
    ax.text(95, 3, f"{slide_num}/{total}", ha="right", va="center",
            fontsize=8, color=GREY, weight="bold")
    # Thin accent bar at top
    ax.add_patch(Rectangle((0, 99.2), 100, 0.8, color=GREEN, lw=0))


def slide_cover():
    fig, ax = new_slide()
    # Top green band
    ax.add_patch(Rectangle((0, 80), 100, 20, color=GREEN, lw=0))
    ax.text(50, 91, "THE SHAPE OF A SKILL", ha="center", va="center",
            fontsize=24, color="white", weight="bold", family="sans-serif")
    ax.text(50, 84, "How ML Skill Demand Bends Across Seniority", ha="center", va="center",
            fontsize=13, color="white", alpha=0.92, style="italic")

    # Three shape icons with labels
    shape_specs = [
        ("Climbing", GREEN, [0.15, 0.40, 0.65, 0.95]),
        ("Mid-peaking", YELLOW, [0.30, 0.95, 0.80, 0.35]),
        ("Dropping", RED, [0.95, 0.65, 0.35, 0.15]),
    ]
    for i, (name, color, pattern) in enumerate(shape_specs):
        base_x = 12 + i * 28
        base_y = 55
        span_x, span_y = 20, 14
        ax.plot([base_x, base_x + span_x], [base_y, base_y], color=GREY, lw=0.8)
        ys = [base_y + v * span_y for v in pattern]
        xs = [base_x + (k / 3) * span_x for k in range(4)]
        ax.plot(xs, ys, color=color, lw=3.2, marker="o", markersize=6)
        ax.text(base_x + span_x / 2, base_y - 4, name, ha="center", va="top",
                fontsize=12, color=color, weight="bold")

    # Body copy
    ax.text(50, 36, "Every skill on your resume has a shape —", ha="center", va="center",
            fontsize=14, color=INK)
    ax.text(50, 32, "peaking at Entry, Mid, Senior, or Staff+ postings.", ha="center", va="center",
            fontsize=14, color=INK)
    ax.text(50, 27, "The shape tells you when to invest, when to coast,", ha="center", va="center",
            fontsize=13, color=GREY, style="italic")
    ax.text(50, 23.5, "and when to let go.", ha="center", va="center",
            fontsize=13, color=GREY, style="italic")

    # Dataset + question teaser
    ax.text(50, 15, "We analyzed 3,277 job postings across DS, MLE, and AI Engineer —", ha="center", va="center",
            fontsize=11, color=INK)
    ax.text(50, 11.5, "and asked which skills actually pay more at fixed seniority.", ha="center", va="center",
            fontsize=11, color=INK)

    ax.text(50, 5.8, "Swipe →", ha="center", va="center",
            fontsize=13, color=GREEN, weight="bold")
    footer(ax, 1, 10)
    return fig


def slide_salary_ladder():
    fig, ax = new_slide()
    ax.text(50, 94, "First, the obvious part.", ha="center", va="top",
            fontsize=20, color=INK, weight="bold")
    ax.text(50, 88, "Seniority drives pay. Let's get that out of the way.", ha="center", va="top",
            fontsize=11, color=GREY, style="italic")

    # Embed the boxplot image from the notebooks repo
    img = mpimg.imread("salary_by_level.png")
    img_ax = fig.add_axes([0.04, 0.22, 0.92, 0.62])
    img_ax.imshow(img)
    img_ax.axis("off")

    # Setup-to-the-real-question callout
    ax.add_patch(FancyBboxPatch((5, 5), 90, 13, boxstyle="round,pad=0.5",
                                 linewidth=0, facecolor=NAVY, alpha=0.08))
    ax.text(50, 13.5, "The interesting question:", ha="center", va="center",
            fontsize=12, color=NAVY, weight="bold")
    ax.text(50, 9, "Which skills separate these levels — and which ones pay more", ha="center", va="center",
            fontsize=11, color=INK)
    ax.text(50, 6, "independent of seniority?", ha="center", va="center",
            fontsize=11, color=INK, style="italic")

    footer(ax, 2, 10)
    return fig


def slide_three_shapes():
    fig, ax = new_slide()
    ax.text(50, 94, "Skills come in 3 shapes.", ha="center", va="top",
            fontsize=22, color=INK, weight="bold")
    ax.text(50, 88, "The pattern a skill makes across seniority levels", ha="center", va="top",
            fontsize=11, color=GREY, style="italic")

    shapes = [
        {"name": "^ Climbing", "color": GREEN,
         "desc": "Peak at Staff+. The skills that actually differentiate you at the top.",
         "example": "e.g. Causal inference, JAX, Evaluation frameworks",
         "pattern": [0.15, 0.35, 0.60, 0.95]},
        {"name": "~ Mid-peaking", "color": YELLOW,
         "desc": "Peak at Mid or Senior, then fade at Staff+. 'Prove-you-know-the-stack' items.",
         "example": "e.g. Python, PyTorch, RAG, LLMs, cloud providers",
         "pattern": [0.35, 0.95, 0.75, 0.40]},
        {"name": "v Dropping", "color": RED,
         "desc": "Peak at Entry. Early-career signatures that fade fast.",
         "example": "e.g. React, APIs, Matplotlib, data pipelines",
         "pattern": [0.95, 0.60, 0.30, 0.15]},
    ]
    # Three horizontal panels
    for i, s in enumerate(shapes):
        y_top = 82 - i * 24
        y_bot = y_top - 20
        # Color band on left
        ax.add_patch(Rectangle((5, y_bot + 2), 3, y_top - y_bot - 4, color=s["color"], lw=0))
        ax.text(10, y_top - 3, s["name"], ha="left", va="top", fontsize=18,
                color=s["color"], weight="bold")
        ax.text(10, y_top - 9, s["desc"], ha="left", va="top", fontsize=11,
                color=INK, wrap=True)
        ax.text(10, y_top - 15, s["example"], ha="left", va="top", fontsize=10,
                color=GREY, style="italic")
        # Mini trajectory chart on the right
        base_x = 75
        base_y = y_bot + 4
        span_x, span_y = 20, 12
        # Baseline axis
        ax.plot([base_x, base_x + span_x], [base_y, base_y], color=GREY, lw=0.8)
        ys = [base_y + v * span_y for v in s["pattern"]]
        xs = [base_x + (k / 3) * span_x for k in range(4)]
        ax.plot(xs, ys, color=s["color"], lw=2.8, marker="o", markersize=5)
        for k, lbl in enumerate(["E", "M", "S", "X"]):
            ax.text(xs[k], base_y - 1.6, lbl, ha="center", va="top", fontsize=7, color=GREY)

    footer(ax, 3, 10)
    return fig


def slide_role_skills(role_label, climbing, mid_peaking, dropping, idx):
    fig, ax = new_slide()
    ax.text(50, 94, f"{role_label}: the level-up skills", ha="center", va="top",
            fontsize=20, color=INK, weight="bold")

    def block(y_top, label, color, items):
        ax.add_patch(Rectangle((5, y_top - 18), 3, 16, color=color, lw=0))
        ax.text(10, y_top - 1.5, label, ha="left", va="top",
                fontsize=14, color=color, weight="bold")
        for j, it in enumerate(items[:4]):
            ax.text(10, y_top - 5.5 - j * 3.2, f"·  {it}", ha="left", va="top",
                    fontsize=11.5, color=INK)

    block(84, "^ CLIMBING  (invest here for Staff+)", GREEN, climbing)
    block(60, "~ MID-PEAKING  (get through, then move on)", YELLOW, mid_peaking)
    block(36, "v DROPPING  (early-career only)", RED, dropping)

    footer(ax, idx, 10)
    return fig


def slide_controlled():
    fig, ax = new_slide()
    ax.text(50, 94, "The plot twist.", ha="center", va="top",
            fontsize=22, color=INK, weight="bold")
    ax.text(50, 88, "Naive $ premium  →  Premium after controlling for seniority", ha="center", va="top",
            fontsize=11, color=GREY, style="italic")

    # Dumbbell chart of 6 key shifts
    shifts = [
        ("Generative AI", 3, -21, RED),
        ("Prompt engineering", -11, -31, RED),
        ("Reinforcement learning", 40, 18, YELLOW),
        ("Fine-tuning", 17, 5, YELLOW),
        ("Kubernetes", 0, 22, GREEN),
        ("Causal inference", 8, 15, GREEN),
    ]
    sub_ax = fig.add_axes([0.28, 0.22, 0.66, 0.52])
    y = np.arange(len(shifts))
    for i, (skill, c1, c2, col) in enumerate(shifts):
        sub_ax.plot([c1, c2], [i, i], color=GREY, lw=1.6, zorder=1)
        sub_ax.scatter(c1, i, s=120, color=YELLOW, edgecolor="white", zorder=3, lw=1.2)
        sub_ax.scatter(c2, i, s=140, color=col, edgecolor="white", zorder=3, lw=1.2)
        # Dollar labels near each endpoint
        sub_ax.text(c2 + (2 if c2 >= 0 else -2), i + 0.3,
                    f"${c2:+d}K".replace("+-", "-"), ha="left" if c2 >= 0 else "right",
                    va="center", fontsize=9, color=col, weight="bold")
    sub_ax.axvline(0, color=INK, lw=0.8, alpha=0.5)
    sub_ax.set_yticks(y)
    sub_ax.set_yticklabels([s[0] for s in shifts], fontsize=11)
    sub_ax.set_xlabel("Salary premium vs baseline (USD, thousands)", fontsize=10)
    sub_ax.set_xlim(-45, 55)
    sub_ax.set_facecolor(BG)
    for s in ["top", "right"]:
        sub_ax.spines[s].set_visible(False)
    sub_ax.tick_params(axis="x", labelsize=9)

    # Legend
    ax.scatter([], [])
    from matplotlib.lines import Line2D
    handles = [
        Line2D([], [], marker="o", color="none", markerfacecolor=YELLOW, markersize=9, label="Naive"),
        Line2D([], [], marker="o", color="none", markerfacecolor=NAVY, markersize=9, label="Controlled"),
    ]
    sub_ax.legend(handles=handles, loc="upper left", fontsize=10, frameon=False,
                  bbox_to_anchor=(0.0, 1.15), ncol=2)

    # Callout
    ax.add_patch(FancyBboxPatch((5, 5), 90, 11, boxstyle="round,pad=0.5",
                                 linewidth=0, facecolor=NAVY, alpha=0.08))
    ax.text(50, 11.5, "Most \"hot AI skill\" premiums are just seniority in disguise.", ha="center", va="center",
            fontsize=12, color=NAVY, weight="bold")
    ax.text(50, 7.5, "Generative AI actually pays LESS at fixed level. Prompt engineering too.", ha="center", va="center",
            fontsize=11, color=INK)

    footer(ax, 7, 10)
    return fig


def slide_winners():
    fig, ax = new_slide()
    ax.text(50, 94, "Skills that actually pay more.", ha="center", va="top",
            fontsize=20, color=INK, weight="bold")
    ax.text(50, 88, "After controlling for role and seniority", ha="center", va="top",
            fontsize=11, color=GREY, style="italic")

    winners = [
        ("JAX", 27, 44),
        ("ETL", 23, 46),
        ("Kubernetes", 22, 42),
        ("Deployment", 19, 39),
        ("Computer vision", 14, 27),
        ("Causal inference", 15, 34),
        ("LLMs", 13, 25),
    ]
    sub_ax = fig.add_axes([0.30, 0.18, 0.63, 0.56])
    y = np.arange(len(winners))[::-1]
    for i, (skill, prem, ci_hi) in enumerate(winners):
        sub_ax.barh(y[i], prem, color=GREEN, alpha=0.85, edgecolor="white")
        sub_ax.text(prem + 1, y[i], f"+${prem}K", va="center", ha="left",
                    fontsize=11, color=GREEN, weight="bold")
    sub_ax.set_yticks(y)
    sub_ax.set_yticklabels([s[0] for s in winners], fontsize=12)
    sub_ax.set_xlim(0, 36)
    sub_ax.set_xlabel("Median salary premium at fixed seniority (USD, thousands)", fontsize=10)
    sub_ax.set_facecolor(BG)
    for s in ["top", "right"]:
        sub_ax.spines[s].set_visible(False)
    sub_ax.tick_params(axis="x", labelsize=9)

    # Context
    ax.text(50, 9, "Infrastructure and foundations beat framework-of-the-month.", ha="center", va="center",
            fontsize=12, color=INK, weight="bold")
    footer(ax, 8, 10)
    return fig


def slide_playbook():
    fig, ax = new_slide()
    ax.text(50, 94, "Level-up playbook.", ha="center", va="top",
            fontsize=22, color=INK, weight="bold")

    plays = [
        ("Mid DS → Senior/Staff", GREEN,
         "Invest in causal inference, A/B testing, experimentation. Skip extra SQL and dashboard work."),
        ("Senior MLE → Staff", GREEN,
         "Go deep: JAX, distributed systems, RL, transformers. MLOps is not the Staff differentiator."),
        ("AI Engineer (any level)", GREEN,
         "Path is evaluation, agents, LLM observability. Prompt engineering is an entry badge, not a staff one."),
        ("Reading the shapes", NAVY,
         "Climbing skills belong on your long-term list. Mid-peaking skills get you through the middle, then fade. Dropping skills should be quietly retired."),
    ]
    for i, (label, color, body) in enumerate(plays):
        y_top = 82 - i * 17
        ax.add_patch(Rectangle((5, y_top - 14), 3, 12, color=color, lw=0))
        ax.text(10, y_top - 1, label, ha="left", va="top",
                fontsize=14, color=color, weight="bold")
        ax.text(10, y_top - 6, body, ha="left", va="top",
                fontsize=11, color=INK, wrap=True)

    footer(ax, 9, 10)
    return fig


def slide_cta():
    fig, ax = new_slide()
    ax.add_patch(Rectangle((0, 72), 100, 28, color=GREEN, lw=0))
    ax.text(50, 88, "Want the full analysis?", ha="center", va="center",
            fontsize=22, color="white", weight="bold")
    ax.text(50, 80, "Tables, methodology, regression CIs, and code.", ha="center", va="center",
            fontsize=13, color="white", alpha=0.92)

    # Blog post
    blog_url = "skillenai.com/2026/04/19/the-senior-to-staff-jump-what-actually-pays-more-in-ml-jobs"
    full_blog = "https://" + blog_url
    ax.text(50, 60, "Full blog post", ha="center", va="center",
            fontsize=13, color=INK, weight="bold")
    ax.text(50, 55, blog_url, ha="center", va="center",
            fontsize=9.5, color=GREEN, family="monospace",
            url=full_blog)

    # GitHub link
    gh_short = "github.com/chiefastro/skillenai-notebooks/tree/master/skill-value-by-seniority"
    gh_full = "https://" + gh_short
    ax.text(50, 43, "Code + data", ha="center", va="center",
            fontsize=13, color=INK, weight="bold")
    ax.text(50, 38, gh_short, ha="center", va="center",
            fontsize=9.5, color=GREEN, family="monospace",
            url=gh_full)

    # Methodology
    ax.text(50, 22, "Methodology:", ha="center", va="center",
            fontsize=11, color=GREY, weight="bold")
    ax.text(50, 17,
            "3,277 postings · chi-square for skill shape · Mann-Whitney for salary",
            ha="center", va="center", fontsize=10, color=GREY)
    ax.text(50, 13,
            "Lasso + OLS hedonic regression for skill premium · US-USD, 515 salaried",
            ha="center", va="center", fontsize=10, color=GREY)

    footer(ax, 10, 10)
    return fig


def main():
    with PdfPages("linkedin-carousel.pdf") as pdf:
        slides = [
            slide_cover(),
            slide_salary_ladder(),
            slide_three_shapes(),
            slide_role_skills("Data Scientist",
                ["Causal inference (9% → 28%)", "A/B testing (9% → 26%)",
                 "Experimentation (3% → 19%)", "Model evaluation (2% → 10%)"],
                ["Python peaks at Mid (78%), fades to 64% at Staff",
                 "SQL peaks Mid (64%), drops to 46% at Staff",
                 "NLP, stats analysis, hypothesis testing peak Mid",
                 "MLOps peaks at Senior (9%), not Staff (2%)"],
                ["Matplotlib (9% → 1%)", "Data pipelines (22% → 11%)",
                 "Data engineering (8% → 6%)"],
                4),
            slide_role_skills("ML Engineer",
                ["JAX (5% → 12% at Senior → Staff)", "Distributed systems (2% → 9%)",
                 "Reinforcement learning (5% → 12%)", "Distributed training (5% → 10%)"],
                ["Python peaks Mid (68%), fades to 48% at Staff",
                 "PyTorch peaks Mid (52%), drops at Staff",
                 "TensorFlow peaks Mid (33%), fades to 21%",
                 "Model serving, monitoring peak at Senior"],
                ["Docker (12% → 5%)", "(Most other drops happen at Staff,",
                 "not Entry — the toolkit is assumed)"],
                5),
            slide_role_skills("AI Engineer",
                ["Evaluation frameworks (2% → 15%)", "Agentic workflows (7% → 15%)",
                 "Observability (11% → 21%)", "Generative AI (4% → 10%)"],
                ["LLMs peak Mid (35%), drop to 16%",
                 "RAG peaks Mid (35%), drop to 16%",
                 "LangChain peaks Senior (21%), drops at Staff",
                 "AWS, GCP, Azure all peak Mid"],
                ["APIs (27% → 3%)", "React (29% → 0%)",
                 "TypeScript (24% → 3%)", "Prompt engineering (29% → 16%)"],
                6),
            slide_controlled(),
            slide_winners(),
            slide_playbook(),
            slide_cta(),
        ]
        for fig in slides:
            pdf.savefig(fig, dpi=DPI, bbox_inches=None)
            plt.close(fig)
    print("Wrote linkedin-carousel.pdf")


if __name__ == "__main__":
    main()
