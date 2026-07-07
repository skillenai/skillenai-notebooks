import pandas as pd, json, numpy as np
fed = pd.read_parquet("federal_tech_hf.parquet")
fed['tl'] = fed.title.str.lower()
N = len(fed)
print("FEDERAL TECH CORPUS N=%d (6 months, 2025-10..2026-03)\n" % N)

# --- SERIES distribution (Abigail's 2210-vs-1560 point) ---
names = {"2210":"IT Management","1550":"Computer Science","1560":"Data Science","0854":"Computer Engineering",
         "0855":"Electronics Eng","1515":"Operations Research","1529":"Math Statistics","1530":"Statistics"}
print("=== OPM SERIES distribution ===")
for s, c in fed.series.value_counts().items():
    print("  %-22s %5d  %4.1f%%" % (names.get(s, s), c, 100*c/N))

# --- within-2210 specialty decomposition ---
s2210 = fed[fed.series == "2210"].copy()
def spec(t):
    if any(w in t for w in ["cyber","infosec","information security","information assurance","security"]): return "Cybersecurity/InfoSec"
    if any(w in t for w in ["data scien","data engineer","data manage","business intel"]): return "Data/Analytics"
    if any(w in t for w in ["software","developer","programmer","application","appsw","web "]): return "Software/App Dev"
    if any(w in t for w in ["network","sysadmin","system admin","systems administ","infrastructure","cloud","server"]): return "Network/Systems/Infra"
    if any(w in t for w in ["customer","help desk","helpdesk","support","service desk"]): return "Customer Support/Helpdesk"
    if any(w in t for w in ["policy","plan","program manage","project manage","govern","enterprise architect","portfolio","cio","chief"]): return "Policy/PM/Mgmt"
    return "Generic IT Specialist"
s2210['spec'] = s2210.tl.map(spec)
print("\n=== WITHIN series 2210 (N=%d, %.0f%% of federal tech) specialty ===" % (len(s2210), 100*len(s2210)/N))
for k, c in s2210.spec.value_counts().items():
    print("  %-28s %5d  %4.1f%%" % (k, c, 100*c/len(s2210)))

# --- FAMILY classification of ALL federal tech (compare to private families) ---
def fam(row):
    t = row.tl; s = row.series
    if s == "1560" or "data scien" in t or ("data" in t and "engineer" in t): return "Data/ML/AI"
    if s in ("1515","1529","1530") or "statistic" in t or "operations research" in t: return "Data/ML/AI"
    if any(w in t for w in ["cyber","infosec","information security","information assurance"]): return "Security/Cyber"
    if any(w in t for w in ["software","developer","programmer","application","appsw"]): return "Software/Dev"
    if any(w in t for w in ["policy","plan","program manage","project manage","govern","portfolio","chief","cio","manager","supervis"]): return "Program/Product/Mgmt"
    if s in ("0854","0855") or any(w in t for w in ["network","sysadmin","system admin","infrastructure","cloud","engineer","architect","electronics"]): return "IT/Ops/Infra"
    return "IT/Ops/Infra"
fed['fam'] = fed.apply(fam, axis=1)
famct = fed.fam.value_counts()
print("\n=== FEDERAL role FAMILY (title/series based) ===")
for k, c in famct.items():
    print("  %-24s %5d  %4.1f%%" % (k, c, 100*c/N))

# --- CLEARANCE moat (structured field) ---
real = fed.clearance.str.title().isin(["Secret","Top Secret","Sensitive Compartmented Information","Confidential","Q Access Authorization","L Access Authorization"])
notreq = fed.clearance.str.title().isin(["Not Required","Public Trust"])
print("\n=== CLEARANCE (structured) ===")
print("  requires real clearance: %d (%.0f%%)" % (real.sum(), 100*real.mean()))
print("  not required:            %d (%.0f%%)" % (notreq.sum(), 100*notreq.mean()))
print("  other/public-trust:      %d (%.0f%%)" % (N-real.sum()-notreq.sum(), 100*(N-real.sum()-notreq.sum())/N))
print("  by family (real-clearance rate):")
for k in famct.index:
    sub = fed[fed.fam == k]
    print("    %-24s %.0f%% (N=%d)" % (k, 100*real[fed.fam == k].mean(), len(sub)))

# --- TELEWORK / REMOTE (structured, newly measurable) ---
print("\n=== TELEWORK / REMOTE (structured) ===")
print("  telework-eligible Yes: %.0f%%" % (100*(fed.telework == "Yes").mean()))
print("  fully-remote job Yes:  %.1f%%" % (100*(fed.remote == "Yes").mean()))

# --- SALARY (structured, annual) ---
ann = fed[(fed.sal_unit == "year") & fed.sal_hi.notna() & (fed.sal_hi > 20000)].copy()
ann['mid'] = (ann.sal_lo + ann.sal_hi)/2
print("\n=== SALARY (annual, structured) N=%d ===" % len(ann))
for q in [10, 25, 50, 75, 90]:
    print("  midpoint p%02d: $%s" % (q, format(int(np.percentile(ann.mid, q)), ',')))
print("  GS grade median: %.0f" % fed.grade.median())

json.dump({"N": N, "series": fed.series.value_counts().to_dict(),
           "spec2210": s2210.spec.value_counts().to_dict(),
           "family": famct.to_dict(),
           "real_clearance_pct": round(100*real.mean(), 1),
           "telework_pct": round(100*(fed.telework == "Yes").mean(), 1),
           "remote_pct": round(100*(fed.remote == "Yes").mean(), 1),
           "salary_mid_pctiles": {q: int(np.percentile(ann.mid, q)) for q in [10, 25, 50, 75, 90]}},
          open("fed_summary.json", "w"), indent=1)
