"""Full analysis for 'not a research role'. Reads the prepped frame, writes every CSV
and fact the report and charts use. Self-contained: no other script's pickles.

    python download.py base_tech.json tech_us.jsonl     # ~62.7K postings, full text
    python prep.py    tech_us.jsonl   tech.pkl
    python analysis.py tech.pkl .
"""
import json, re, sys
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint, proportions_ztest
from flags import add_flags, PAT

SRC, OUT = sys.argv[1], sys.argv[2]
ORDER = ["AI Engineer","ML Engineer","Data Scientist","Research/Applied Scientist",
         "Data Engineer","Data Analyst","Software Engineer"]

df = add_flags(pd.read_pickle(SRC))
df = df[~df["is_spam"]].copy()                      # spam employer (carpet-bombing)
df["f_strict"] = df["text"].fillna("").str.contains(PAT["anti_research_strict"], regex=True)
df["lq"]  = pd.qcut(df["tlen"], 5, labels=["Q1","Q2","Q3","Q4","Q5"])
# employer-name normalisation BEFORE any concentration check (variants bias it downward)
df["empn"] = df["companyCanonicalName"].fillna("").str.lower().map(
    lambda e: re.sub(r"[^a-z0-9]","",e).replace("andurilindustries","anduril").replace("testnisc","nisc"))

# ---------------------------------------------------------------- 1. prevalence
rows=[]
for g in ORDER:
    s=df[df["grp"]==g]; n=len(s)
    for lab,col in [("anti_research_strict","f_strict"),("anti_research_broad","f_anti_research"),
                    ("research_positive","f_research_positive"),("evals","f_evals"),
                    ("ship_register","f_ship_register"),("phd","f_phd")]:
        k=int(s[col].sum()); lo,hi=proportion_confint(k,n,method="wilson")
        rows.append({"role_group":g,"register":lab,"n_postings":n,"k":k,"pct":round(100*k/n,2),
                     "ci_lo":round(100*lo,2),"ci_hi":round(100*hi,2)})
pd.DataFrame(rows).to_csv(f"{OUT}/prevalence_by_role.csv",index=False)

# robustness: near-duplicate boilerplate, and the employer as the unit
df["thash"] = df["text"].str.slice(0, 4000).map(hash)
dd = df.drop_duplicates(["empn", "thash"])
emp = df[df["empn"]!=""].groupby("empn")[["f_strict","f_research_positive"]].max()

# ---------------------------------------------------------------- 2. pay
p = df[df["pay_ok"] & df["grp"].notna() & df["level"].notna() & df["locationAdmin1"].notna()
       & df["platform"].notna() & df["workModel"].notna()].copy()
p["ly"] = np.log(p["mid"])
big = p[p["empn"].map(p["empn"].value_counts()) >= 3]
FIT = ["f_strict","f_pipeline","f_ship_register","f_prod_grade","f_research_any",
       "f_experimentation","f_evals","f_stats_rigor","f_phd","f_placebo_eoe","f_placebo_dent","f_llm"]
# cross-sectional: cannot hold the employer constant, so it absorbs employer identity (see placebos)
m_cs = smf.ols("ly ~ "+" + ".join(FIT)+" + C(level)+C(grp)+C(lq)+C(platform)+C(workModel)+C(locationAdmin1)",
               data=p).fit(cov_type="cluster",cov_kwds={"groups":p["empn"]})
# within-employer: the calibrated specification
m_fe = smf.ols("ly ~ "+" + ".join(FIT)+" + C(level)+C(grp)+C(lq)+C(empn)",
               data=big).fit(cov_type="cluster",cov_kwds={"groups":big["empn"]})
rows=[]
for f in FIT+["f_anti_research"]:
    on,off=p.loc[p[f],"mid"],p.loc[~p[f],"mid"]
    r={"register":f,"n_on":int(p[f].sum()),"naive_median_on":int(on.median()),
       "naive_median_off":int(off.median()),"naive_pct":round(100*(on.median()/off.median()-1),2)}
    for m,tag in [(m_cs,"cs"),(m_fe,"fe")]:
        k=f+"[T.True]"
        if k in m.params:
            b,se=m.params[k],m.bse[k]
            r|={f"{tag}_pct":round(100*(np.exp(b)-1),2),f"{tag}_lo":round(100*(np.exp(b-1.96*se)-1),2),
                f"{tag}_hi":round(100*(np.exp(b+1.96*se)-1),2),f"{tag}_p":round(m.pvalues[k],4)}
    rows.append(r)
pd.DataFrame(rows).to_csv(f"{OUT}/pay_effects.csv",index=False)

# ---------------------------------------------------------------- 3. co-occurrence
rows=[]
for g in ORDER:
    s=df[df["grp"]==g]; a=s[s["f_strict"]]
    if len(a)<10: continue
    rows.append({"role_group":g,"n_anti":len(a),"n_all":len(s),
        "evals_in_anti":round(100*a["f_evals"].mean(),1),"evals_base":round(100*s["f_evals"].mean(),1),
        "rpos_in_anti":round(100*a["f_research_positive"].mean(),1),
        "rpos_base":round(100*s["f_research_positive"].mean(),1)})
pd.DataFrame(rows).to_csv(f"{OUT}/cooccurrence.csv",index=False)

# LLM-matched: removes the "is this an AI job at all" confound
rows=[]
for g in ["Software Engineer","ML Engineer","AI Engineer","Data Scientist"]:
    s=df[(df["grp"]==g)&df["f_llm"]]; a=s[s["f_strict"]]; b=s[~s["f_strict"]]
    if len(a)<10: continue
    z,pv=proportions_ztest([a["f_evals"].sum(),b["f_evals"].sum()],[len(a),len(b)])
    lo,hi=proportion_confint(int(a["f_evals"].sum()),len(a),method="wilson")
    rows.append({"role_group":g,"n_anti_llm":len(a),"n_other_llm":len(b),
        "evals_in_anti":round(100*a["f_evals"].mean(),1),"ci_lo":round(100*lo,1),"ci_hi":round(100*hi,1),
        "evals_in_other":round(100*b["f_evals"].mean(),1),"z":round(z,2),"p":round(pv,4),
        "rpos_in_anti":round(100*a["f_research_positive"].mean(),1),
        "rpos_in_other":round(100*b["f_research_positive"].mean(),1)})
pd.DataFrame(rows).to_csv(f"{OUT}/cooccurrence_llm_matched.csv",index=False)

# ---------------------------------------------------------------- 4. register mix
out=[]
for d_,lab in [(p,"all tech"),(p[p["grp"].isin(ORDER[:4])],"AI/ML/DS")]:
    d_=d_.copy()
    d_["PROD"]=d_["f_ship_register"]|d_["f_prod_grade"]|d_["f_strict"]|d_["f_pipeline"]
    d_["cell"]=np.where(d_.PROD&d_.f_research_positive,"both",
               np.where(d_.PROD,"production only",
               np.where(d_.f_research_positive,"research only","neither")))
    g=d_.groupby("cell")["mid"].agg(["size","median"])
    mm=smf.ols("ly ~ C(cell, Treatment('neither'))+C(level)+C(grp)+C(lq)+C(platform)+C(workModel)+C(locationAdmin1)",
               data=d_).fit(cov_type="cluster",cov_kwds={"groups":d_["empn"]})
    for c in ["neither","production only","research only","both"]:
        r={"scope":lab,"cell":c,"n":int(g.loc[c,"size"]),"median_pay":int(g.loc[c,"median"])}
        k=f"C(cell, Treatment('neither'))[T.{c}]"
        if k in mm.params:
            b,se=mm.params[k],mm.bse[k]
            r|={"pct_vs_neither":round(100*(np.exp(b)-1),2),"ci_lo":round(100*(np.exp(b-1.96*se)-1),2),
                "ci_hi":round(100*(np.exp(b+1.96*se)-1),2),"p":round(mm.pvalues[k],4)}
        out.append(r)
    if lab=="AI/ML/DS":
        ref=pd.DataFrame([{"level":"Senior","grp":"AI Engineer","platform":"greenhouse","workModel":"hybrid",
                           "locationAdmin1":"California","lq":"Q4","cell":c} for c in
                          ["neither","production only","research only","both"]])
        ref["lq"]=pd.Categorical(ref["lq"],categories=["Q1","Q2","Q3","Q4","Q5"])
        PRED={c:int(v) for c,v in zip(ref["cell"],np.exp(mm.predict(ref)))}
pd.DataFrame(out).to_csv(f"{OUT}/pay_by_register_mix.csv",index=False)

# ---------------------------------------------------------------- 5. facts
a=df[df["f_strict"]]; e=df[df["f_evals"]]
sl=df[df["f_llm"]]; sa=sl[sl["f_strict"]]; sb=sl[~sl["f_strict"]]
z,pv=proportions_ztest([sa["f_evals"].sum(),sb["f_evals"].sum()],[len(sa),len(sb)])
F={"postings":len(df),"employers":int(df["empn"].nunique()),"median_chars":int(df["tlen"].median()),
   "distinct_texts":int(len(dd)),
   "salaried_n":len(p),"salaried_employers":int(p["empn"].nunique()),
   "salaried_median_pay":int(p["mid"].median()),
   "fe_n":int(m_fe.nobs),"fe_employers":int(big["empn"].nunique()),
   "fe_adj_r2":round(m_fe.rsquared_adj,3),"cs_adj_r2":round(m_cs.rsquared_adj,3),
   "anti_strict_n":len(a),"anti_strict_employers":int(a["empn"].nunique()),
   "anti_top_employer":a["empn"].value_counts().index[0],
   "anti_top_share":round(100*a["empn"].value_counts().iloc[0]/len(a),1),
   "anti_llm_share":round(100*a["f_llm"].mean(),1),
   "evals_n":len(e),"evals_employers":int(e["empn"].nunique()),
   "evals_top_employer":e["empn"].value_counts().index[0],
   "evals_top_share":round(100*e["empn"].value_counts().iloc[0]/len(e),1),
   "evals_llm_share":round(100*e["f_llm"].mean(),1),
   "anti_all_tech_pct":round(100*df["f_strict"].mean(),2),
   "rpos_all_tech_pct":round(100*df["f_research_positive"].mean(),1),
   "employer_level_anti":round(100*emp["f_strict"].mean(),2),
   "employer_level_rpos":round(100*emp["f_research_positive"].mean(),2),
   "llm_matched_pooled":{"anti_n":len(sa),"anti_evals":round(100*sa["f_evals"].mean(),1),
        "other_n":len(sb),"other_evals":round(100*sb["f_evals"].mean(),1),
        "z":round(z,2),"p":float(pv)},
   "predicted_senior_aie_ca":PRED}
for x,y in [("f_evals","f_ship_register"),("f_evals","f_strict")]:
    t=m_fe.t_test(f"{x}[T.True] - {y}[T.True] = 0"); d=float(np.squeeze(t.effect))
    F[f"contrast_{x}_minus_{y}"]={"pct":round(100*(np.exp(d)-1),2),
                                  "p":round(float(np.squeeze(t.pvalue)),4)}
# length-standardised prevalence (longer ads contain more of everything)
w=df["lq"].value_counts(normalize=True)
F["length_standardised_anti"]={g: round(100*(df[df.grp==g].groupby("lq",observed=True)["f_strict"].mean()*w).sum(),2)
                               for g in ORDER}
json.dump(F,open(f"{OUT}/facts.json","w"),indent=1,default=str)
print(json.dumps(F,indent=1,default=str))
