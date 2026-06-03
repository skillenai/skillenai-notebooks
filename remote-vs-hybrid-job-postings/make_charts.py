#!/usr/bin/env python3
"""
Render the two charts for the remote-vs-hybrid job-posting analysis from
workmodel_results.json:

  chart_seniority.png  - work model mix by seniority level (stacked bar)
  chart_country.png    - hybrid share of postings by country

Usage:  python3 make_charts.py   (run query_workmodel.py first)
"""
import json
import matplotlib.pyplot as plt
import numpy as np

d = json.load(open("workmodel_results.json"))

REMOTE, HYBRID, ONSITE = "#2563eb", "#f59e0b", "#cbd5e1"


def wm_pct(bucket):
    wm = {x["key"]: x["doc_count"] for x in bucket["wm"]["buckets"]}
    tot = wm.get("remote", 0) + wm.get("hybrid", 0) + wm.get("onsite", 0)
    return (100 * wm.get("remote", 0) / tot,
            100 * wm.get("hybrid", 0) / tot,
            100 * wm.get("onsite", 0) / tot, tot)


# ---- Chart 1: work model by seniority ----------------------------------
LADDER = ["intern", "entry", "mid", "senior", "staff", "principal",
          "lead", "manager", "director", "vp", "c-level"]
LABELS = {"intern": "Intern", "entry": "Entry", "mid": "Mid", "senior": "Senior",
          "staff": "Staff", "principal": "Principal", "lead": "Lead",
          "manager": "Manager", "director": "Director", "vp": "VP", "c-level": "C-level"}
sen = {b["key"]: b for b in d["by_sen"]["buckets"]}
rows = [(LABELS[k], *wm_pct(sen[k])) for k in LADDER if k in sen]

names = [r[0] for r in rows]
rem = np.array([r[1] for r in rows])
hyb = np.array([r[2] for r in rows])
ons = np.array([r[3] for r in rows])
y = np.arange(len(names))[::-1]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(y, rem, color=REMOTE, label="Remote")
ax.barh(y, hyb, left=rem, color=HYBRID, label="Hybrid")
ax.barh(y, ons, left=rem + hyb, color=ONSITE, label="Onsite")
for i, yy in enumerate(y):
    ax.text(rem[i] / 2, yy, f"{rem[i]:.0f}%", va="center", ha="center",
            color="white", fontsize=9, fontweight="bold")
    ax.text(rem[i] + hyb[i] / 2, yy, f"{hyb[i]:.0f}%", va="center", ha="center",
            color="white", fontsize=9, fontweight="bold")
ax.set_yticks(y)
ax.set_yticklabels(names)
ax.set_xlim(0, 100)
ax.set_xlabel("Share of job postings (%)")
ax.set_title("Flexibility is earned: work model by seniority\n"
             "166,039 job postings, Skillenai index, May 2026",
             fontsize=12, fontweight="bold")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("chart_seniority.png", dpi=150, bbox_inches="tight")
plt.close()
print("wrote chart_seniority.png")

# ---- Chart 2: hybrid share by country ----------------------------------
NAMES = {"US": "United States", "IN": "India", "GB": "United Kingdom",
         "CA": "Canada", "DE": "Germany", "BR": "Brazil", "FR": "France",
         "SG": "Singapore", "PL": "Poland", "ES": "Spain", "AU": "Australia",
         "IL": "Israel"}
EUROPE = {"GB", "DE", "FR", "ES", "PL"}
crows = []
for b in d["by_country"]["buckets"]:
    r, h, o, tot = wm_pct(b)
    crows.append((b["key"], h, tot))
crows.sort(key=lambda x: x[1], reverse=True)

labels = [NAMES.get(c, c) for c, _, _ in crows]
vals = [h for _, h, _ in crows]
colors = ["#16a34a" if c in EUROPE else "#94a3b8" for c, _, _ in crows]
yy = np.arange(len(labels))[::-1]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(yy, vals, color=colors)
for i, v in zip(yy, vals):
    ax.text(v + 0.4, i, f"{v:.1f}%", va="center", fontsize=9)
ax.set_yticks(yy)
ax.set_yticklabels(labels)
ax.set_xlabel("Hybrid share of job postings (%)")
ax.set_title("“Hybrid” is mostly a European arrangement\n"
             "Hybrid share of postings by country, Skillenai index, May 2026",
             fontsize=12, fontweight="bold")
ax.set_xlim(0, max(vals) + 5)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color="#16a34a", label="Europe"),
                    Patch(color="#94a3b8", label="Rest of world")],
          loc="lower right", frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("chart_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("wrote chart_country.png")
