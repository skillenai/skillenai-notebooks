"""Apply skill_merge_map.json to jobs.csv and write jobs_merged.csv.

Each job's skill list gets deduplicated after remapping.
"""
import csv
import json

m = json.load(open("skill_merge_map.json"))

rows_out = []
with open("jobs.csv") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    for row in reader:
        skills = [s for s in (row["skills"] or "").split("|") if s]
        mapped = []
        seen = set()
        for s in skills:
            canon = m.get(s, s)
            if canon not in seen:
                seen.add(canon)
                mapped.append(canon)
        row["skills"] = "|".join(mapped)
        rows_out.append(row)

with open("jobs_merged.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows_out)

# Sanity: count unique skills before and after
before = set()
after = set()
with open("jobs.csv") as f:
    for row in csv.DictReader(f):
        for s in (row["skills"] or "").split("|"):
            if s:
                before.add(s)
for row in rows_out:
    for s in (row["skills"] or "").split("|"):
        if s:
            after.add(s)
print(f"Unique skills before merge: {len(before)}")
print(f"Unique skills after merge:  {len(after)}")
print(f"Wrote jobs_merged.csv with {len(rows_out)} jobs")
