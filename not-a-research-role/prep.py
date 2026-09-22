"""Build the analysis frame: cleaned text, role family, level, pay, text length."""
import json, re, sys
import pandas as pd, numpy as np
from textutil import clean

SRC, OUT = sys.argv[1], sys.argv[2]
rows=[]
for line in open(SRC):
    d=json.loads(line)
    d["text"]=clean(d.pop("extractedText",None))
    rows.append(d)
df=pd.DataFrame(rows)
print("raw rows:", len(df))

LEVEL_WORDS = r"(?:senior|sr\.?|staff|principal|distinguished|lead|junior|jr\.?|entry[- ]level|entry|associate|mid[- ]level|intermediate|chief|head of|vp of|director of|manager of|ii|iii|iv|i)"
def family(role):
    if not isinstance(role,str) or not role.strip(): return None
    r=role.strip().lower()
    r=re.sub(r"[,(].*$","",r)
    r=re.sub(r"\s*[-|/]\s*(?:remote|hybrid|onsite|us|usa).*$","",r)
    for _ in range(3):
        r=re.sub(rf"^{LEVEL_WORDS}\s+","",r).strip()
        r=re.sub(rf"\s+{LEVEL_WORDS}$","",r).strip()
    r=re.sub(r"\s+"," ",r)
    for pat,rep in [(r"^full[\s-]?stack","full stack"),(r"^fullstack","full stack"),
        (r"^machine learning\b","ml"),(r"^artificial intelligence\b","ai"),(r"^ai/ml\b","ml"),
        (r"^front[\s-]?end","frontend"),(r"^back[\s-]?end","backend"),(r"^dev ?ops","devops"),
        (r"^sre$","site reliability engineer"),(r"^software development engineer","software engineer"),
        (r"^software dev engineer","software engineer")]:
        r=re.sub(pat,rep,r)
    r=re.sub(r"\bsoftware developer\b","software engineer",r)
    r=re.sub(r"\bdeveloper\b","engineer",r)
    return r.strip()
df["family"]=df["role"].map(family)

# coarse discipline group for reporting
def group(f):
    if not isinstance(f,str): return None
    if re.search(r"\b(research scientist|research engineer|ai researcher|ai scientist|ml scientist|machine learning scientist|applied scientist|ai research)\b", f): return "Research/Applied Scientist"
    if re.search(r"\b(data scientist|data science)\b", f): return "Data Scientist"
    if re.search(r"\b(ai engineer|applied ai engineer|ai software engineer|generative ai engineer|ai platform engineer|ai infrastructure engineer)\b", f): return "AI Engineer"
    if re.search(r"\b(ml engineer|deep learning engineer|mlops engineer|ml infrastructure engineer|ml platform engineer|nlp engineer|computer vision engineer)\b", f): return "ML Engineer"
    if re.search(r"\b(data engineer|analytics engineer|data architect|business intelligence)\b", f): return "Data Engineer"
    if re.search(r"\bdata analyst\b", f): return "Data Analyst"
    if re.search(r"\b(software engineer|backend engineer|frontend engineer|full stack engineer|platform engineer|infrastructure engineer)\b", f): return "Software Engineer"
    return "Other tech"
df["grp"]=df["family"].map(group)

IC={"entry":"Entry","junior":"Entry","mid":"Mid","senior":"Senior","staff":"Staff+","principal":"Staff+"}
df["level"]=df["seniorityLevel"].map(lambda s: IC.get(s.strip().lower()) if isinstance(s,str) else None)

mn=pd.to_numeric(df["salaryMin"],errors="coerce"); mx=pd.to_numeric(df["salaryMax"],errors="coerce")
unit=np.where(mx.isna(),"na",np.where(mx<=300,"hourly",np.where(mx<=5000,"ambiguous","annual")))
df["_unit"]=unit
mn=np.where(unit=="hourly",mn*2080,mn); mx=np.where(unit=="hourly",mx*2080,mx)
df["mid"]=(mn+mx)/2
usd = df["salaryCurrency"].eq("USD")
ok = pd.Series(unit).isin(["hourly","annual"]).values & usd.values & (mx>=mn) & df["mid"].between(30_000,1_200_000).values
df["pay_ok"]=ok
df.loc[~ok,"mid"]=np.nan
df["is_spam"]=df["companyCanonicalName"].fillna("").str.lower().eq("speechify")
df["tlen"]=df["text"].str.len()
print(df["grp"].value_counts().to_string())
print("\npay_ok:",int(ok.sum()), " median mid:", np.nanmedian(df["mid"]))
print("\ntext length deciles:", np.percentile(df["tlen"],[10,25,50,75,90]).round().tolist())
df.to_pickle(OUT); print("wrote",OUT)
