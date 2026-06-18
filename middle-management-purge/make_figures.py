#!/usr/bin/env python3
"""Generate figures for the middle-management-purge analysis.

Data sourced from prod-enriched-jobs (US, ex-Speechify), 2026-06-17.
Counts hard-coded from the API aggregations run during the session; the
company scatter reads the saved aggregation at /tmp/co_agg.json.
"""
import json
import math
from statistics import mean
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/Users/jrand/git-repos/skillenai-notebooks/.claude/worktrees/middle-management-purge/middle-management-purge"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
GREY = "#64748b"
RED = "#dc2626"

# ---------------------------------------------------------------------------
# Figure 1: any-remote % by seniority level (the two-ladder / valley chart)
# US, ex-Speechify. (N, any-remote%)
# ---------------------------------------------------------------------------
sen = [
    ("Entry",     5421, 40.9, "ic"),
    ("Mid",       7280, 51.0, "ic"),
    ("Senior",   31454, 52.8, "ic"),
    ("Staff",     7298, 62.3, "ic"),
    ("Principal", 4224, 50.9, "ic"),
    ("Lead",      5933, 40.1, "mgmt"),
    ("Manager",   7556, 52.1, "mgmt"),
    ("Director",  2240, 52.1, "mgmt"),
    ("VP",         684, 48.0, "exec"),
    ("C-level",    298, 43.0, "exec"),
]
labels = [s[0] for s in sen]
vals = [s[2] for s in sen]
colors = [BLUE if s[3] == "ic" else (ORANGE if s[3] == "mgmt" else RED) for s in sen]

fig, ax = plt.subplots(figsize=(12, 6.2))
bars = ax.bar(range(len(sen)), vals, color=colors, edgecolor="white", linewidth=0.8)
for i, (lab, n, v, _) in enumerate(sen):
    ax.text(i, v + 0.8, f"{v:.0f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.text(i, 2.0, f"n={n:,}", ha="center", va="bottom", fontsize=7.5, color="white", rotation=0)
ax.set_xticks(range(len(sen)))
ax.set_xticklabels(labels, fontsize=10.5)
ax.set_ylabel("Jobs offering remote or hybrid work (%)", fontsize=11)
ax.set_ylim(0, 70)
ax.axhline(52.8, color=GREY, ls="--", lw=1, alpha=0.6)
ax.set_title("The remote-work valley: mid-senior ICs work remotely the most;\nexecutives among the least — on par with entry-level",
             fontsize=14, fontweight="bold", loc="left")
# Legend
from matplotlib.patches import Patch
ax.legend(handles=[
    Patch(color=BLUE, label="Individual contributor"),
    Patch(color=ORANGE, label="Management track"),
    Patch(color=RED, label="Executive"),
], loc="upper right", fontsize=9.5, framealpha=0.9)
ax.spines[["top", "right"]].set_visible(False)
ax.text(0.0, -0.13, "US postings, Speechify excluded · prod-enriched-jobs · Skillenai",
        transform=ax.transAxes, fontsize=8, color=GREY)
plt.tight_layout()
plt.savefig(f"{OUT}/01_remote_by_seniority.png", dpi=150, bbox_inches="tight")
plt.close()
print("wrote 01_remote_by_seniority.png")

# ---------------------------------------------------------------------------
# Figure 2: management density by work model (clean vs lead-contaminated)
# ---------------------------------------------------------------------------
modes = ["Remote", "Hybrid", "Onsite"]
clean = [0.167, 0.200, 0.177]
withlead = [0.246, 0.290, 0.312]

x = np.arange(len(modes))
w = 0.38
fig, ax = plt.subplots(figsize=(9.5, 6))
b1 = ax.bar(x - w/2, clean, w, label="Clean (manager + director)", color=BLUE)
b2 = ax.bar(x + w/2, withlead, w, label='Including inflated "Lead" title', color=GREY, alpha=0.65)
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.004,
                f"{b.get_height():.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(modes, fontsize=11)
ax.set_ylabel("Managers per individual contributor (MGMT : IC)", fontsize=11)
ax.set_ylim(0, 0.36)
ax.set_title("Remote postings are NOT flatter: management density is\nessentially constant across work models",
             fontsize=14, fontweight="bold", loc="left")
ax.legend(fontsize=10, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.text(0.0, -0.12, 'The apparent "remote = flat" gap vanishes once the inflated "Lead" catch-all is removed.',
        transform=ax.transAxes, fontsize=8.5, color=GREY)
plt.tight_layout()
plt.savefig(f"{OUT}/02_mgmt_density_by_workmodel.png", dpi=150, bbox_inches="tight")
plt.close()
print("wrote 02_mgmt_density_by_workmodel.png")

# ---------------------------------------------------------------------------
# Figure 3: within-engineering "no cliff" test
# ---------------------------------------------------------------------------
tiers = ["Senior IC\n(engineer)", "Staff/Principal IC\n(engineer)", "Management\n(Eng Mgr / Dir / VP)"]
anyremote = [59.4, 66.9, 66.1]
ns = [9623, 3728, 2467]
cols = [BLUE, BLUE, ORANGE]
fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.bar(range(3), anyremote, color=cols, edgecolor="white", width=0.6)
for i, (v, n) in enumerate(zip(anyremote, ns)):
    ax.text(i, v + 0.7, f"{v:.1f}%", ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax.text(i, 3, f"n={n:,}", ha="center", va="bottom", fontsize=8.5, color="white")
ax.set_xticks(range(3))
ax.set_xticklabels(tiers, fontsize=10.5)
ax.set_ylabel("Jobs offering remote or hybrid work (%)", fontsize=11)
ax.set_ylim(0, 76)
ax.annotate("", xy=(2, 70), xytext=(1, 70),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
ax.text(1.5, 71, "no cliff: 0.8 pp", ha="center", color=GREEN, fontsize=10, fontweight="bold")
ax.set_title("Holding job family constant, becoming a manager costs\nbasically zero remote work",
             fontsize=14, fontweight="bold", loc="left")
ax.spines[["top", "right"]].set_visible(False)
ax.text(0.0, -0.14, "US engineering postings, Speechify excluded · prod-enriched-jobs · Skillenai",
        transform=ax.transAxes, fontsize=8, color=GREY)
plt.tight_layout()
plt.savefig(f"{OUT}/03_engineering_no_cliff.png", dpi=150, bbox_inches="tight")
plt.close()
print("wrote 03_engineering_no_cliff.png")

# ---------------------------------------------------------------------------
# Figure 4: company-level scatter remote_share vs mgmt_share
# ---------------------------------------------------------------------------
d = json.load(open("/tmp/co_agg.json"))
IC = {"entry", "mid", "senior", "staff", "principal"}
MGMT = {"manager", "director"}
rows = []
for c in d["aggregations"]["co"]["buckets"]:
    wm = {b["key"]: b["doc_count"] for b in c["wm"]["buckets"]}
    s = {b["key"]: b["doc_count"] for b in c["sen"]["buckets"]}
    r, o, h = wm.get("remote", 0), wm.get("onsite", 0), wm.get("hybrid", 0)
    wmt = r + o + h
    ic = sum(s.get(k, 0) for k in IC)
    mg = sum(s.get(k, 0) for k in MGMT)
    base = ic + mg
    if wmt < 40 or base < 40:
        continue
    rows.append((c["key"], c["doc_count"], r / wmt, mg / base))

xs = np.array([r[2] for r in rows]) * 100
ys = np.array([r[3] for r in rows]) * 100
sizes = np.array([r[1] for r in rows])

def spearman(a, b):
    n = len(a)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    ra = ra.astype(float); rb = rb.astype(float)
    return np.corrcoef(ra, rb)[0, 1]

rho = spearman(xs, ys)

fig, ax = plt.subplots(figsize=(10, 6.5))
ax.scatter(xs, ys, s=np.clip(sizes / 3, 15, 400), alpha=0.45, color=BLUE, edgecolor="white", linewidth=0.5)
# trend line (OLS on raw)
m, bb = np.polyfit(xs, ys, 1)
xx = np.linspace(0, 100, 50)
ax.plot(xx, m * xx + bb, color=RED, lw=2, ls="--")
ax.set_xlabel("Share of a company's postings that are fully remote (%)", fontsize=11)
ax.set_ylabel("Management share of a company's postings (%)", fontsize=11)
ax.set_xlim(-3, 103)
ax.set_ylim(0, min(60, ys.max() + 5))
ax.set_title(f"Remote-first companies are not flatter\nSpearman ρ = +{rho:.2f} (weak, wrong direction for the 'remote kills managers' thesis)",
             fontsize=13.5, fontweight="bold", loc="left")
ax.spines[["top", "right"]].set_visible(False)
ax.text(0.0, -0.13, f"Each bubble = one company (≥ 40 US postings, n={len(rows)}). Bubble size ∝ posting volume · Skillenai",
        transform=ax.transAxes, fontsize=8, color=GREY)
plt.tight_layout()
plt.savefig(f"{OUT}/04_company_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"wrote 04_company_scatter.png (n={len(rows)}, rho=+{rho:.3f})")
print(f"  onsite-first mean mgmt_share: {mean(r[3] for r in sorted(rows,key=lambda x:x[2])[:len(rows)//3]):.3f}")
print(f"  remote-first mean mgmt_share: {mean(r[3] for r in sorted(rows,key=lambda x:x[2])[-len(rows)//3:]):.3f}")
