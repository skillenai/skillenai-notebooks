"""
Remote pay and geography: does working remotely change what you're paid,
or only whose location sets it?

Prep conventions (pay-unit normalization, role-family and seniority bucketing) are
deliberately identical to the tech-role-pay-2026 analysis in this repo so the two
are directly comparable.

Usage: python3 analysis.py <postings.csv> <outdir>
"""
import json, re, sys
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import pearsonr
from scipy import stats

SRC, OUT = sys.argv[1], sys.argv[2]
df = pd.read_csv(SRC)
print(f"raw rows: {len(df):,}")
R = {}

# ---- 1. pay-unit normalization (same rule as tech-role-pay-2026) ----------
mn = pd.to_numeric(df["salaryMin"], errors="coerce")
mx = pd.to_numeric(df["salaryMax"], errors="coerce")
df["_mn"], df["_mx"] = mn, mx
def unit(v):
    if pd.isna(v): return "na"
    if v <= 300: return "hourly"
    if v <= 5000: return "ambiguous"     # weekly / biweekly / monthly - undecidable
    return "annual"
df["_unit"] = mx.map(unit)
print("\npay-unit classification:")
print(df["_unit"].value_counts().to_string())
# Does the unit mix differ by work model? (a differential drop would bias the comparison)
print("\nunit mix by work model (%):")
print((pd.crosstab(df["workModel"], df["_unit"], normalize="index")*100).round(2).to_string())
R["unit_mix_by_workmodel"] = (pd.crosstab(df["workModel"], df["_unit"], normalize="index")*100).round(3).to_dict()

hourly = df["_unit"] == "hourly"
df.loc[hourly, ["_mn","_mx"]] = df.loc[hourly, ["_mn","_mx"]] * 2080
df["mid"] = (df["_mn"] + df["_mx"]) / 2

drop = {}
keep = df["_unit"].isin(["hourly","annual"])
drop["ambiguous_or_missing_unit"] = int((~keep).sum())
keep &= df["_mx"] >= df["_mn"]
keep &= df["mid"].between(30_000, 1_200_000)
drop["implausible_annual_midpoint"] = int(len(df) - drop["ambiguous_or_missing_unit"] - keep.sum())
keep &= df["workModel"].isin(["onsite","remote","hybrid"])
df = df[keep].copy()
print("\ndrops:", json.dumps(drop, indent=1))
print(f"clean rows: {len(df):,}")
R["drops"] = drop; R["n_clean"] = int(len(df))

# ---- 2. role family normalization ---------------------------------------
LEVEL_WORDS = (r"(?:senior|sr\.?|staff|principal|distinguished|lead|junior|jr\.?|"
               r"entry[- ]level|entry|associate|mid[- ]level|intermediate|chief|head of|"
               r"vp of|director of|manager of|ii|iii|iv|i)")
def family(role):
    if not isinstance(role, str) or not role.strip(): return None
    r = role.strip().lower()
    r = re.sub(r"[,(].*$", "", r)
    r = re.sub(r"\s*[-|/]\s*(?:remote|hybrid|onsite|us|usa).*$", "", r)
    for _ in range(3):
        r = re.sub(rf"^{LEVEL_WORDS}\s+", "", r).strip()
        r = re.sub(rf"\s+{LEVEL_WORDS}$", "", r).strip()
    r = re.sub(r"\s+", " ", r)
    for pat, rep in [(r"^full[\s-]?stack","full stack"), (r"^fullstack","full stack"),
                     (r"^machine learning\b","ml"), (r"^artificial intelligence\b","ai"),
                     (r"^ai/ml\b","ml"), (r"^front[\s-]?end","frontend"),
                     (r"^back[\s-]?end","backend"), (r"^dev ?ops","devops"),
                     (r"^sre$","site reliability engineer"),
                     (r"^software development engineer","software engineer"),
                     (r"^software dev engineer","software engineer")]:
        r = re.sub(pat, rep, r)
    r = re.sub(r"\bsoftware developer\b", "software engineer", r)
    r = re.sub(r"\bdeveloper\b", "engineer", r)
    return r.strip()
df["family"] = df["role"].map(family)
topf = df["family"].value_counts().head(80).index
df["fam_c"] = np.where(df["family"].isin(topf), df["family"], "OTHER")

# ---- 3. seniority buckets (intern + lead excluded, as in the companion) ---
IC = {"entry":"Entry","junior":"Entry","mid":"Mid","senior":"Senior",
      "staff":"Staff+","principal":"Staff+"}
MGMT = {"manager":"Management","director":"Management","vp":"Exec","c-level":"Exec"}
def bucket(s):
    if not isinstance(s, str): return None
    s = s.strip().lower()
    return IC.get(s) or MGMT.get(s)
df["level"] = df["seniorityLevel"].map(bucket)
df = df[df["level"].notna()].copy()
print(f"rows with a usable level bucket: {len(df):,}")
print(df["level"].value_counts().to_string())

df["state"] = df["locationAdmin1"].fillna("").replace("", "UNSPECIFIED")
df["logpay"] = np.log(df["mid"])
df["band_rel"] = (df["_mx"] - df["_mn"]) / df["mid"]
df["co"] = df["companyCanonicalName"].fillna("").str.strip().str.lower()
R["n_model"] = int(len(df))

# ---- 4. naive ------------------------------------------------------------
print("\n=== NAIVE pay by work model ===")
naive = df.groupby("workModel")["mid"].agg(["count","median","mean",
        lambda s: s.quantile(.25), lambda s: s.quantile(.75)])
naive.columns = ["n","median","mean","p25","p75"]
print(naive.round(0).to_string())
b = naive.loc["onsite","median"]
R["naive"] = {k: {kk: round(float(vv),1) for kk, vv in v.items()} for k, v in naive.to_dict("index").items()}
for wm in ("remote","hybrid"):
    R["naive"][wm]["vs_onsite_pct"] = round(100*(naive.loc[wm,"median"]/b-1), 2)
    print(f"  {wm} vs onsite: {100*(naive.loc[wm,'median']/b-1):+.1f}%")

# ---- 5. stepwise control build-up ---------------------------------------
print("\n=== STEPWISE: remote coefficient as controls are added ===")
specs = [("raw (no controls)", "logpay ~ C(workModel, Treatment('onsite'))"),
         ("+ seniority", "logpay ~ C(workModel, Treatment('onsite')) + C(level)"),
         ("+ role family", "logpay ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c)"),
         ("+ platform", "logpay ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c) + C(platform)"),
         ("+ state (full)", "logpay ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c) + C(platform) + C(state)")]
step = []
for lab, f in specs:
    m = smf.ols(f, data=df).fit(cov_type="HC1")
    k = [x for x in m.params.index if "workModel" in x and "remote" in x][0]
    se = m.bse[k]; c = m.params[k]
    pct, lo, hi = (100*(np.exp(c)-1), 100*(np.exp(c-1.96*se)-1), 100*(np.exp(c+1.96*se)-1))
    step.append({"spec": lab, "pct": round(pct,2), "lo": round(lo,2), "hi": round(hi,2)})
    print(f"  {lab:20s} remote = {pct:+.2f}% [{lo:+.2f}%, {hi:+.2f}%]")
R["stepwise"] = step

FULL = ("logpay ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c) "
        "+ C(platform) + C(state)")
mfull = smf.ols(FULL, data=df).fit(cov_type="HC1")
print(f"\nfull model N={int(mfull.nobs):,} R2={mfull.rsquared:.3f}")
R["full_r2"] = round(mfull.rsquared, 4); R["full_n"] = int(mfull.nobs)
R["full"] = {}
for k in mfull.params.index:
    if "workModel" in k:
        lab = k.split("T.")[-1].rstrip("]"); c, se = mfull.params[k], mfull.bse[k]
        R["full"][lab] = {"pct": round(100*(np.exp(c)-1),2),
                          "lo": round(100*(np.exp(c-1.96*se)-1),2),
                          "hi": round(100*(np.exp(c+1.96*se)-1),2), "p": float(mfull.pvalues[k])}
        print(f"  {lab:7s} {R['full'][lab]['pct']:+.2f}% "
              f"[{R['full'][lab]['lo']:+.2f}%, {R['full'][lab]['hi']:+.2f}%]  p={mfull.pvalues[k]:.2e}")

# ---- 6. platform disagreement (the honest caveat) ------------------------
print("\n=== Remote coefficient BY PLATFORM (instrument disagreement check) ===")
rob = []
for p in sorted(df["platform"].dropna().unique()):
    s = df[df["platform"] == p]
    if len(s) < 2000: continue
    m = smf.ols("logpay ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c) + C(state)",
                data=s).fit(cov_type="HC1")
    k = [x for x in m.params.index if "workModel" in x and "remote" in x][0]
    c, se = m.params[k], m.bse[k]
    rob.append({"platform": p, "n": int(len(s)), "pct": round(100*(np.exp(c)-1),2),
                "lo": round(100*(np.exp(c-1.96*se)-1),2), "hi": round(100*(np.exp(c+1.96*se)-1),2)})
    print(f"  {p:12s} n={len(s):6,}  remote={rob[-1]['pct']:+.2f}% "
          f"[{rob[-1]['lo']:+.2f}%, {rob[-1]['hi']:+.2f}%]")
R["platform_robustness"] = rob

# ---- 7. IC-only ----------------------------------------------------------
ic = df[df["level"].isin(["Entry","Mid","Senior","Staff+"])]
mic = smf.ols(FULL, data=ic).fit(cov_type="HC1")
R["ic_only"] = {}
print(f"\n=== IC-only (n={int(mic.nobs):,}) ===")
for k in mic.params.index:
    if "workModel" in k:
        lab = k.split("T.")[-1].rstrip("]"); c, se = mic.params[k], mic.bse[k]
        R["ic_only"][lab] = {"pct": round(100*(np.exp(c)-1),2),
                             "lo": round(100*(np.exp(c-1.96*se)-1),2),
                             "hi": round(100*(np.exp(c+1.96*se)-1),2)}
        print(f"  {lab:7s} {R['ic_only'][lab]['pct']:+.2f}% "
              f"[{R['ic_only'][lab]['lo']:+.2f}%, {R['ic_only'][lab]['hi']:+.2f}%]")

# ---- 8. GEOGRAPHY --------------------------------------------------------
# Residualize on role family + level + platform only; no state, no work model.
mr = smf.ols("logpay ~ C(fam_c) + C(level) + C(platform)", data=df).fit()
df["resid"] = mr.resid
MIN_N = 150
def prem(wm):
    s = df[(df["workModel"] == wm) & (df["state"] != "UNSPECIFIED")]
    g = s.groupby("state")["resid"].agg(["count","mean"])
    return g[g["count"] >= MIN_N]

print("\n=== GEOGRAPHIC DISPERSION (weighted SD of state effect) ===")
disp = []
for wm in ("onsite","hybrid","remote"):
    g = prem(wm)
    if len(g) < 5: continue
    w = g["count"]; mu = np.average(g["mean"], weights=w)
    sd = np.sqrt(np.average((g["mean"]-mu)**2, weights=w))
    disp.append({"wm": wm, "n_states": int(len(g)), "n": int(w.sum()), "sd_pct": round(100*float(sd),2)})
    print(f"  {wm:7s} states={len(g):2d} n={int(w.sum()):6,}  SD={100*sd:.2f}%")
R["dispersion"] = disp

print("\n=== PASS-THROUGH vs onsite (hybrid = placebo; it requires commuting) ===")
o = prem("onsite"); pt = {}
for wm in ("hybrid","remote"):
    g = prem(wm); common = o.index.intersection(g.index)
    if len(common) < 5: continue
    x, y = o.loc[common,"mean"].values, g.loc[common,"mean"].values
    w = np.minimum(o.loc[common,"count"].values, g.loc[common,"count"].values)
    d2 = pd.DataFrame({"x":x,"y":y,"w":w})
    fit = smf.wls("y ~ x", data=d2, weights=d2["w"]).fit()
    bb, se = fit.params["x"], fit.bse["x"]; ci = fit.conf_int().loc["x"]; r = pearsonr(x,y)
    dfree = len(common)-2
    p0 = float(2*(1-stats.t.cdf(abs(bb/se), dfree)))
    p1 = float(2*(1-stats.t.cdf(abs((bb-1)/se), dfree)))
    pt[wm] = {"slope": round(float(bb),3), "lo": round(float(ci[0]),3), "hi": round(float(ci[1]),3),
              "r": round(float(r[0]),3), "sd_ratio": round(float(np.std(y)/np.std(x)),3),
              "n_states": int(len(common)), "p_vs_0": round(p0,4), "p_vs_1": round(p1,4)}
    print(f"  {wm:7s} slope={bb:.3f} [{ci[0]:.3f},{ci[1]:.3f}] r={r[0]:.3f} "
          f"SDratio={np.std(y)/np.std(x):.3f} states={len(common)}  "
          f"p(slope=0)={p0:.4f}  p(slope=1)={p1:.3f}")
R["passthrough"] = pt

# state table
rows = []
for st in o.index.intersection(prem("remote").index):
    oo, rr = o.loc[st], prem("remote").loc[st]
    rows.append({"state": st, "n_onsite": int(oo["count"]),
                 "onsite_prem_pct": round(100*(np.exp(oo["mean"])-1),2),
                 "n_remote": int(rr["count"]),
                 "remote_prem_pct": round(100*(np.exp(rr["mean"])-1),2)})
gt = pd.DataFrame(rows).sort_values("onsite_prem_pct", ascending=False)
gt["gap_pp"] = (gt["onsite_prem_pct"] - gt["remote_prem_pct"]).round(2)
print("\n=== State residual pay premium by work mode ===")
print(gt.to_string(index=False))
gt.to_csv(f"{OUT}/state_premiums.csv", index=False)
R["state_table"] = gt.to_dict("records")

# ---- 9. is the anchor the EMPLOYER's location? ---------------------------
print("\n=== Is a remote posting's state the EMPLOYER's location? ===")
om = (df[(df["workModel"]=="onsite") & (df["state"]!="UNSPECIFIED")]
      .groupby("co")["state"].agg(lambda s: s.value_counts().idxmax()))
on = df[df["workModel"]=="onsite"].groupby("co").size()
om = om[om.index.isin(on[on>=3].index)]
sd_ = df[df["state"]!="UNSPECIFIED"]["state"].value_counts(normalize=True)
R["anchor"] = {"n_companies": int(len(om))}
for wm in ("remote","hybrid"):
    s = df[(df["workModel"]==wm)&(df["state"]!="UNSPECIFIED")&(df["co"].isin(om.index))].copy()
    s["hq"] = s["co"].map(om)
    match = float((s["state"]==s["hq"]).mean())
    chance = float(sum(sd_.get(x,0) for x in s["hq"])/len(s))
    R["anchor"][wm] = {"n": int(len(s)), "match_pct": round(100*match,2),
                       "chance_pct": round(100*chance,2)}
    print(f"  {wm:7s} n={len(s):6,}  anchor==employer modal onsite state: "
          f"{100*match:.1f}%  (chance {100*chance:.1f}%)")

# how much of the remote geo gradient is WHICH COMPANY vs location banding?
rem = df[(df["workModel"]=="remote") & (df["state"]!="UNSPECIFIED")].copy()
bc = rem["co"].value_counts(); rem = rem[rem["co"].isin(bc[bc>=5].index)]
ks = rem["state"].value_counts(); rem = rem[rem["state"].isin(ks[ks>=100].index)]
def ssd(m): return float(np.std([v for k,v in m.params.items() if k.startswith("C(state)")]))
m1 = smf.ols("logpay ~ C(state) + C(fam_c) + C(level) + C(platform)", data=rem).fit()
m2 = smf.ols("logpay ~ C(state) + C(fam_c) + C(level) + C(platform) + C(co)", data=rem).fit()
absorbed = 100*(1-ssd(m2)/ssd(m1))
print(f"\n  remote state-effect SD without company FE: {ssd(m1):.4f}")
print(f"  remote state-effect SD with    company FE: {ssd(m2):.4f}")
print(f"  -> {absorbed:.1f}% of the remote geographic gradient is WHICH COMPANY is hiring;")
print(f"     the remainder is location banding inside firms (n={len(rem):,}, "
      f"{rem['co'].nunique()} companies, {rem['state'].nunique()} states)")
R["company_fe"] = {"sd_no_fe": round(ssd(m1),4), "sd_with_fe": round(ssd(m2),4),
                   "pct_absorbed": round(absorbed,2), "n": int(len(rem)),
                   "n_companies": int(rem["co"].nunique()), "n_states": int(rem["state"].nunique())}

# ---- 10. band width ------------------------------------------------------
print("\n=== Relative band width (max-min)/mid ===")
bw = df.groupby("workModel")["band_rel"].agg(["count","median","mean"])
print((bw*[1,100,100]).round(2).to_string())
mb = smf.ols("band_rel ~ C(workModel, Treatment('onsite')) + C(level) + C(fam_c) + C(platform) + C(state)",
             data=df).fit(cov_type="HC1")
R["band"] = {"naive": {k: {"n": int(v["count"]), "median_pct": round(100*v["median"],2),
                           "mean_pct": round(100*v["mean"],2)} for k,v in bw.to_dict("index").items()},
             "controlled_pp": {}}
for k in mb.params.index:
    if "workModel" in k:
        lab = k.split("T.")[-1].rstrip("]")
        R["band"]["controlled_pp"][lab] = {"pp": round(100*mb.params[k],2), "p": float(mb.pvalues[k])}
        print(f"  controlled {lab:7s} {100*mb.params[k]:+.2f} pp  p={mb.pvalues[k]:.2e}")

# ---- exports -------------------------------------------------------------
pd.DataFrame(step).to_csv(f"{OUT}/stepwise_controls.csv", index=False)
pd.DataFrame(rob).to_csv(f"{OUT}/platform_robustness.csv", index=False)
piv = df.pivot_table(index="level", columns="workModel", values="mid", aggfunc="median")
cnt = df.pivot_table(index="level", columns="workModel", values="mid", aggfunc="count")
piv.join(cnt, rsuffix="_n").to_csv(f"{OUT}/pay_by_level_workmode.csv")
R["by_level"] = piv.round(0).to_dict()
R["by_level_n"] = cnt.to_dict()
(pd.crosstab(df["workModel"], df["level"], normalize="index")*100).round(2).to_csv(
    f"{OUT}/level_mix_by_workmode.csv")
R["level_mix"] = (pd.crosstab(df["workModel"], df["level"], normalize="index")*100).round(2).to_dict()
json.dump(R, open(f"{OUT}/results.json","w"), indent=1, default=str)
print(f"\nwrote results.json + CSVs to {OUT}")

# ---- 11. sensitivity: drop Maryland (defense/clearance composition) -------
print("\n=== SENSITIVITY: pass-through excluding Maryland ===")
md = df[df["state"]=="Maryland"]
print("  MD onsite top employers:",
      ", ".join(f"{k}({v})" for k,v in
                md[md.workModel=="onsite"]["companyCanonicalName"].value_counts().head(5).items()))
sens = {}
for wm in ("hybrid","remote"):
    g = prem(wm); common = o.index.intersection(g.index).drop("Maryland", errors="ignore")
    if len(common) < 5: continue
    x, y = o.loc[common,"mean"].values, g.loc[common,"mean"].values
    w = np.minimum(o.loc[common,"count"].values, g.loc[common,"count"].values)
    d2 = pd.DataFrame({"x":x,"y":y,"w":w})
    fit = smf.wls("y ~ x", data=d2, weights=d2["w"]).fit()
    bb, se = fit.params["x"], fit.bse["x"]; ci = fit.conf_int().loc["x"]; r = pearsonr(x,y)
    dfree = len(common)-2
    sens[wm] = {"slope": round(float(bb),3), "lo": round(float(ci[0]),3),
                "hi": round(float(ci[1]),3), "r": round(float(r[0]),3),
                "sd_ratio": round(float(np.std(y)/np.std(x)),3), "n_states": int(len(common)),
                "p_vs_0": round(float(2*(1-stats.t.cdf(abs(bb/se),dfree))),4),
                "p_vs_1": round(float(2*(1-stats.t.cdf(abs((bb-1)/se),dfree))),4)}
    print(f"  {wm:7s} slope={bb:.3f} [{ci[0]:.3f},{ci[1]:.3f}] r={r[0]:.3f} "
          f"SDratio={np.std(y)/np.std(x):.3f} states={len(common)} "
          f"p(0)={sens[wm]['p_vs_0']:.4f} p(1)={sens[wm]['p_vs_1']:.3f}")
R["passthrough_noMD"] = sens
json.dump(R, open(f"{OUT}/results.json","w"), indent=1, default=str)
print("results.json updated")
