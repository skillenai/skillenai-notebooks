"""Rank skills by job-vs-blog coverage gap and print clean table."""
import json
from pathlib import Path

d = json.loads(Path("/tmp/prevalence.json").read_text())
totals = d["totals"]
JOB = "prod-enriched-jobs"
BLOG = "prod-enriched-blog"

# Drop unreliable concepts (match_phrase analyzer kills C++/C#; weak disambig kills Excel/Bash/R/Cursor)
EXCLUDE = {"C++", "C#", "Excel", "Bash", "R (language)", "Cursor (editor)"}

rows = []
for label in d["results"][JOB]:
    if label in EXCLUDE:
        continue
    jc = d["results"][JOB].get(label, 0)
    bc = d["results"][BLOG].get(label, 0)
    if jc < 50 or bc < 50:
        continue
    jrate = jc / totals[JOB] * 10000
    brate = bc / totals[BLOG] * 10000
    ratio = jrate / brate if brate else float("inf")
    rows.append({"label": label, "jobs": jc, "blog": bc, "jobs_per_10k": jrate, "blog_per_10k": brate, "job_blog_ratio": ratio})

rows.sort(key=lambda r: -r["job_blog_ratio"])

print(f"{'rank':>4}  {'skill':28}  {'jobs':>7}  {'jobs/10k':>9}  {'blog':>7}  {'blog/10k':>9}  {'ratio':>6}")
print("-" * 84)
for i, r in enumerate(rows, 1):
    print(f"{i:>4}  {r['label']:28}  {r['jobs']:>7,}  {r['jobs_per_10k']:>9.1f}  {r['blog']:>7,}  {r['blog_per_10k']:>9.1f}  {r['job_blog_ratio']:>6.2f}")

# Save
Path("/tmp/ranked_skills.json").write_text(json.dumps(rows, indent=2))
print(f"\nUNDER-COVERED top 12 (high job:blog ratio = high demand, low blog supply):")
for r in rows[:12]:
    print(f"  {r['label']:25}  ratio {r['job_blog_ratio']:.2f}  (jobs {r['jobs']:,} / blog {r['blog']:,})")

print(f"\nOVER-COVERED bottom 12 (low job:blog ratio = lots of blogs, less job demand):")
for r in rows[-12:]:
    print(f"  {r['label']:25}  ratio {r['job_blog_ratio']:.2f}  (jobs {r['jobs']:,} / blog {r['blog']:,})")
