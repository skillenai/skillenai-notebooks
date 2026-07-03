"""Federal side of the public-vs-private tech 'broken bargain' analysis.

Uses the opm-fwd-skill client. Produces:
  federal_pay.csv        new-hire (accessions) + incumbent (employment) pay percentiles by role
  federal_seniority.csv  GS-grade -> entry/mid/senior buckets by role
  federal_stability.csv  monthly tech quit rate 2023-2026 + tenure
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/git-repos/opm-fwd-skill/scripts"))
os.environ.setdefault("OPM_FWD_CACHE", "/tmp/opm_verify_cache_2")
import fwd, pandas as pd, numpy as np

# Clean role maps only (federal occupational series -> Skillenai posted role)
ROLES = {
    "Data Scientist": ["1560"],
    "Software Engineer / IT": ["2210", "1550"],   # IT Mgmt + Computer Science
    "Computer Science (1550)": ["1550"],
    "IT Management (2210)": ["2210"],
}
TECH = {"1560", "2210", "1550", "0854", "1515", "1530"}

def wpct(df, col, ps):
    df = df.dropna(subset=[col]); df = df[(df["count"] > 0) & (df[col] > 0)]
    a = df.sort_values(col); c = a["count"].cumsum(); tot = a["count"].sum()
    return {p: float(a.loc[c >= p/100*tot, col].iloc[0]) for p in ps}

# ---- PAY: federal new-hire (accessions 2024, normal hiring year) + incumbent (employment 2026-05)
def pay_frame(dataset, year_months):
    frames = []
    for y, m in year_months:
        d = fwd.load(dataset, y, m)
        d["pay"] = pd.to_numeric(d["annualized_adjusted_basic_pay"], errors="coerce")
        d = d[(d["duty_station_country_code"] == "US")]
        frames.append(d)
    return pd.concat(frames, ignore_index=True)

acc24 = pay_frame("accessions", [(2024, m) for m in range(1, 13)])   # new hires
emp = pay_frame("employment", [(2026, 5)])                            # incumbents

rows = []
for role, codes in ROLES.items():
    a = acc24[acc24.occupational_series_code.isin(codes)]
    e = emp[emp.occupational_series_code.isin(codes)]
    ap = wpct(a, "pay", [10,25,50,75,90]); ep = wpct(e, "pay", [10,25,50,75,90])
    rows.append({"role": role,
                 "newhire_n": int(a["count"].sum()),
                 "newhire_p25": ap.get(25), "newhire_p50": ap.get(50), "newhire_p75": ap.get(75), "newhire_p90": ap.get(90),
                 "incumbent_n": int(e["count"].sum()),
                 "incumbent_p25": ep.get(25), "incumbent_p50": ep.get(50), "incumbent_p75": ep.get(75), "incumbent_p90": ep.get(90)})
pay = pd.DataFrame(rows); pay.to_csv("federal_pay.csv", index=False)
print("=== FEDERAL PAY (new-hire 2024 accessions vs incumbent 2026-05) ===")
print(pay.to_string(index=False))

# ---- TENURE medians (pre-disruption 2024-12 vs now); stability series live in analyze_stability.py
def wmed(df,col):
    df=df.dropna(subset=[col]); df=df[df["count"]>0]
    a=df.sort_values(col); c=a["count"].cumsum(); return float(a.loc[c>=0.5*a["count"].sum(),col].iloc[0])
print("\n=== FEDERAL TECH TENURE (median length of service) ===")
for y,m in [(2024,12),(2026,5)]:
    e=fwd.load("employment",y,m); e["los"]=pd.to_numeric(e["length_of_service_years"],errors="coerce")
    tech=e[e.occupational_series_code.isin(TECH)]
    print(f"  {y}-{m:02d}: tech median = {wmed(tech,'los'):.1f}y")
print("\nsaved: federal_pay.csv")
