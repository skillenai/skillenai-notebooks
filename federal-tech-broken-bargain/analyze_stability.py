"""Stability leg: mobility (quits) vs security (involuntary loss), and the pension hinge.

Outputs:
  federal_involuntary.csv   monthly federal RIF rate (all + tech), annualized
  stability_by_age.csv      2024 quit rate by age + retirement counts (tech + all federal)
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/git-repos/opm-fwd-skill/scripts"))
os.environ.setdefault("OPM_FWD_CACHE", "/tmp/opm_verify_cache_2")
import fwd, pandas as pd

TECH = {"1560", "2210", "1550", "0854", "1515", "1530"}
AGES = ["LESS THAN 20","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65 OR MORE"]

hc_all = int(fwd.load("employment", 2024, 12)["count"].sum())
hc_tech = int(fwd.load("employment", 2024, 12)[lambda d: d.occupational_series_code.isin(TECH)]["count"].sum())

# ---- Involuntary (RIF) rate time series
rows = []
for y in (2023, 2024, 2025, 2026):
    for m in range(1, 13):
        if y == 2026 and m > 5: break
        d = fwd.load("separations", y, m)
        rif_all = int(d[d.separation_category_code == "SH"]["count"].sum())
        t = d[d.occupational_series_code.isin(TECH)]
        rif_t = int(t[t.separation_category_code == "SH"]["count"].sum())
        sc_t = int(t[t.separation_category_code == "SC"]["count"].sum())
        rows.append({"month": f"{y}-{m:02d}",
                     "rif_all": rif_all, "rif_rate_all_ann": 100*rif_all*12/hc_all,
                     "rif_tech": rif_t, "rif_rate_tech_ann": 100*rif_t*12/hc_tech,
                     "quit_rate_tech_ann": 100*sc_t*12/hc_tech})
inv = pd.DataFrame(rows); inv.to_csv("federal_involuntary.csv", index=False)
print("=== Federal RIF rate (annualized %), selected months ===")
print(inv[inv.month.isin(["2024-06","2025-06","2025-09","2026-05"])].to_string(index=False))

# ---- Age curves (2024): quit rate by age + retirements by age
def hc_by_age(codes):
    e = fwd.load("employment", 2024, 12); e = e[e.occupational_series_code.isin(codes)]
    return e.groupby("age_bracket")["count"].sum()
def sep_by_age(cat, codes):
    tot = pd.Series(0.0, index=AGES)
    for m in range(1, 13):
        d = fwd.load("separations", 2024, m); d = d[d.occupational_series_code.isin(codes)]
        if cat: d = d[d.separation_category_code == cat]
        tot = tot.add(d.groupby("age_bracket")["count"].sum(), fill_value=0)
    return tot

arows = []
codes = list(TECH)
hc = hc_by_age(codes); sc = sep_by_age("SC", codes); sd = sep_by_age("SD", codes)
for a in AGES:
    h = hc.get(a, 0)
    arows.append({"age": a, "headcount": int(h), "quits": int(sc.get(a, 0)),
                  "quit_rate_pct": (100*sc.get(a, 0)/h if h else 0), "retirements": int(sd.get(a, 0))})
age = pd.DataFrame(arows); age.to_csv("stability_by_age.csv", index=False)
print("\n=== Federal TECH: 2024 quit rate by age + retirements ===")
print(age.to_string(index=False))
print("\nsaved: federal_involuntary.csv, stability_by_age.csv")
