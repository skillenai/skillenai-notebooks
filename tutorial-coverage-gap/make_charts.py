"""Generate report charts for the under-covered skills analysis."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = Path("/tmp/charts")
OUT.mkdir(parents=True, exist_ok=True)

rows = json.loads(Path("/tmp/ranked_skills.json").read_text())
gap_authors = json.loads(Path("/tmp/gap_authors.json").read_text())

# ---------- Chart 1: ranked under/over coverage ----------
sorted_rows = sorted(rows, key=lambda r: r["job_blog_ratio"])
labels = [r["label"] for r in sorted_rows]
ratios = [r["job_blog_ratio"] for r in sorted_rows]
median_ratio = float(np.median(ratios))

# Color by tier
def color_for(ratio):
    if ratio < 1.5:
        return "#d04545"  # over-covered (red)
    if ratio > 5.0:
        return "#2a7d4f"  # severely under-covered (deep green)
    if ratio > median_ratio:
        return "#7eb88f"  # moderately under-covered (light green)
    return "#bdbdbd"      # neutral grey

colors = [color_for(r) for r in ratios]

fig, ax = plt.subplots(figsize=(11, 16))
y = np.arange(len(labels))
ax.barh(y, ratios, color=colors, edgecolor="white", linewidth=0.5)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel("Job-to-blog coverage ratio  (jobs per 10k ÷ blog mentions per 10k)", fontsize=10)
ax.set_title("The tutorial coverage gap, 74 skills\nhigh ratio = high job demand, low blog supply",
             fontsize=13, loc="left", pad=15)
ax.axvline(median_ratio, color="black", linestyle="--", linewidth=1, alpha=0.5)
ax.text(median_ratio + 0.1, len(labels) - 1, f"median {median_ratio:.1f}",
        fontsize=9, color="black", va="top")
ax.axvline(1.0, color="black", linewidth=0.8, alpha=0.3)
for i, r in enumerate(ratios):
    ax.text(r + 0.1, i, f"{r:.2f}", va="center", fontsize=8, color="#333")
ax.set_xlim(0, max(ratios) * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
patches = [
    mpatches.Patch(color="#2a7d4f", label="ratio > 5  — severely under-covered"),
    mpatches.Patch(color="#7eb88f", label=f"ratio > {median_ratio:.1f} (median) — under-covered"),
    mpatches.Patch(color="#bdbdbd", label="ratio 1.5–median — near-typical"),
    mpatches.Patch(color="#d04545", label="ratio < 1.5 — over-covered by bloggers"),
]
ax.legend(handles=patches, loc="lower right", fontsize=9, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "01_coverage_ratio.png", dpi=150)
plt.close()

# ---------- Chart 2: AI vs BI bucket ----------
BUCKETS = {
    "BI tools": ["Looker", "Tableau", "Power BI"],
    "DataOps plumbing": ["Airflow", "Terraform", "Jenkins", "DBT", "Ansible"],
    "JVM ecosystem": ["Kotlin", "Scala", "Spring Boot", "Java"],
    "AI / LLM topics": ["Claude Code", "LLM", "RAG", "Generative AI", "fine-tuning", "LangChain", "prompt engineering", "MLOps", "machine learning"],
}
by_label = {r["label"]: r for r in rows}

fig, ax = plt.subplots(figsize=(12, 7))
bucket_names = list(BUCKETS.keys())
bucket_colors = {"BI tools": "#2a7d4f", "DataOps plumbing": "#7eb88f", "JVM ecosystem": "#a3a3d1", "AI / LLM topics": "#d04545"}
y_pos = 0
yticks = []
ytick_labels = []
for bn in bucket_names:
    skills = [s for s in BUCKETS[bn] if s in by_label]
    skills.sort(key=lambda s: by_label[s]["job_blog_ratio"], reverse=True)
    for s in skills:
        ratio = by_label[s]["job_blog_ratio"]
        ax.barh(y_pos, ratio, color=bucket_colors[bn], edgecolor="white")
        ax.text(ratio + 0.1, y_pos, f"{ratio:.2f}", va="center", fontsize=9)
        yticks.append(y_pos)
        ytick_labels.append(s)
        y_pos += 1
    y_pos += 0.5  # gap between buckets
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels, fontsize=10)
ax.invert_yaxis()
ax.axvline(median_ratio, color="black", linestyle="--", linewidth=1, alpha=0.5)
ax.text(median_ratio + 0.15, len(yticks) * 0.6, f"median across\nall 74 skills: {median_ratio:.1f}",
        fontsize=9, color="black", ha="left", va="center")
ax.axvline(1.0, color="black", linewidth=0.8, alpha=0.3)
ax.text(1.0 + 0.05, len(yticks) * 0.85, "1.0 = blogs and jobs\nmention equally often",
        fontsize=8, color="#555", ha="left", va="center")
ax.set_xlabel("Job-to-blog coverage ratio", fontsize=10)
ax.set_title("Where bloggers spend their time vs. where employers spend their job posts",
             fontsize=13, loc="left", pad=15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
patches = [mpatches.Patch(color=v, label=k) for k, v in bucket_colors.items()]
ax.legend(handles=patches, loc="lower right", fontsize=10, frameon=False)
plt.tight_layout()
plt.savefig(OUT / "02_bucket_comparison.png", dpi=150)
plt.close()

# ---------- Chart 3: top multi-skill gap-fillers ----------
multi = gap_authors["multi_skill_gap_fillers"][:12]
# Re-rank by total_posts within multi-skill set
multi.sort(key=lambda r: -r["total_posts"])

skills_order = ["Looker", "Tableau", "Power BI", "Kotlin", "Scala", "Spring Boot", "GCP", "Airflow", "Terraform", "Jenkins", "DBT", "Ansible"]
fig, ax = plt.subplots(figsize=(14, 7))
nA, nS = len(multi), len(skills_order)
mat = np.zeros((nA, nS), dtype=int)
for i, a in enumerate(multi):
    for s in a["skills"]:
        if s["skill"] in skills_order:
            mat[i, skills_order.index(s["skill"])] = s["posts"]

# Log color scale (the matrix has values 0–208)
display = np.log1p(mat)
im = ax.imshow(display, cmap="Greens", aspect="auto")
ax.set_xticks(range(nS))
ax.set_xticklabels(skills_order, rotation=35, ha="right", fontsize=10)
ax.set_yticks(range(nA))
ax.set_yticklabels([f"{a['author']}\n@{a['top_domain']}" for a in multi], fontsize=9)
ax.set_title("Who's actually writing about the under-served skills?\nblog post counts per author × skill",
             fontsize=13, loc="left", pad=15)
for i in range(nA):
    for j in range(nS):
        v = mat[i, j]
        if v > 0:
            ax.text(j, i, str(v), ha="center", va="center", fontsize=8,
                    color="white" if v > 30 else "#222")
ax.set_xlabel("under-covered skill", fontsize=10)
plt.tight_layout()
plt.savefig(OUT / "03_gap_fillers.png", dpi=150)
plt.close()

# ---------- Chart 4: scatter plot - jobs vs blog with labels ----------
fig, ax = plt.subplots(figsize=(12, 9))
xs = [r["blog_per_10k"] for r in rows]
ys = [r["jobs_per_10k"] for r in rows]
ratios = [r["job_blog_ratio"] for r in rows]
labels = [r["label"] for r in rows]

# Color points by ratio
def scatter_color(r):
    if r < 1.5: return "#d04545"
    if r > 5.0: return "#2a7d4f"
    if r > median_ratio: return "#7eb88f"
    return "#bdbdbd"

ax.scatter(xs, ys, c=[scatter_color(r) for r in ratios], s=60, alpha=0.85, edgecolor="white", linewidth=0.5)

# diagonal lines: ratio = 1, ratio = median, ratio = 5
mx = max(max(xs), max(ys)) * 1.1
xline = np.linspace(0.5, mx, 100)
ax.plot(xline, xline * 1.0, "--", color="black", linewidth=1, alpha=0.4, label="ratio = 1")
ax.plot(xline, xline * median_ratio, "--", color="#7eb88f", linewidth=1, alpha=0.7, label=f"ratio = {median_ratio:.1f} (median)")
ax.plot(xline, xline * 5.0, "--", color="#2a7d4f", linewidth=1, alpha=0.7, label="ratio = 5")

# Label notable skills
to_label = set([r["label"] for r in sorted_rows[:8]] + [r["label"] for r in sorted_rows[-8:]] +
               ["Looker", "Tableau", "Power BI", "Airflow", "Terraform", "GCP",
                "Claude Code", "LLM", "RAG", "Generative AI", "fine-tuning",
                "Python", "AWS", "machine learning"])
for r in rows:
    if r["label"] in to_label:
        ax.annotate(r["label"], (r["blog_per_10k"], r["jobs_per_10k"]),
                    fontsize=8, alpha=0.85, ha="left", va="bottom",
                    xytext=(4, 2), textcoords="offset points")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Blog mentions per 10,000 posts  (log scale)", fontsize=10)
ax.set_ylabel("Job mentions per 10,000 postings  (log scale)", fontsize=10)
ax.set_title("Job demand vs blog supply — 74 skills",
             fontsize=13, loc="left", pad=15)
ax.legend(loc="lower right", fontsize=9, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUT / "04_scatter.png", dpi=150)
plt.close()

print("wrote:")
for p in sorted(OUT.glob("*.png")):
    print(f"  {p}  ({p.stat().st_size//1024}KB)")
