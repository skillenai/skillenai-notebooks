"""Add the software QA/SDET family; drop the discipline-mixed Test Engineer bucket."""
import pandas as pd, numpy as np, json
df=pd.read_parquet("clean3.parquet")

SW_QA={"QA Engineer","Quality Assurance Engineer","Software QA Engineer","QA Automation Engineer",
 "Test Automation Engineer","Automation Test Engineer","Software Test Engineer",
 "Software Development Engineer in Test","Software Development Engineer in Test (SDET)",
 "Software Engineer in Test","Software Developer in Test","Software Quality Assurance Engineer",
 "Software Quality Engineer","Performance Test Engineer","SDET","QA Test Engineer",
 "Quality Assurance Automation Engineer"}
r=df.role.fillna("")
sel = r.isin(SW_QA) | r.str.match(
    r"^(?:Senior|Sr\.?|Staff|Principal|Lead|Junior|Associate)\s+(?:QA|SDET|Software QA|Quality Assurance)\b",
    case=False)
df.loc[sel,"family"]="qa / sdet engineer"
df.to_parquet("clean4.parquet")

sen=df[df.level=="Senior"]
gate={}
for f,s in sen.groupby("family"):
    if len(s)<60: continue
    vc=s.emp.value_counts()
    gate[f]=dict(n=len(s),n_emp=len(vc),top=vc.iloc[0]/len(s)*100,top_emp=vc.index[0])

# Definitional exclusions, each with its reason recorded at the moment of choosing it.
DEFN={
 "engineering manager":"92.9% people-management - reported in the management band instead",
 "it specialist":"federal job-series classification, not a market role title",
 "test engineer":"DISCIPLINE-MIXED: top skill term is 'manufacturing' 25.6% vs Selenium 6.7%, "
                 "pytest/junit 1.6%; top employers are hardware/aerospace. Cannot be attributed "
                 "cleanly to software or hardware test, so it is not comparable to the rest of the board.",
}
keep=[f for f,g in gate.items() if g["n_emp"]>=10 and g["top"]<=25 and f not in DEFN]
json.dump({"keep":keep,"defn_exclusions":DEFN},open("keep4.json","w"),indent=2)
print(f"FINAL: {len(keep)} families (was 28)")
for f in ("qa / sdet engineer","software engineer in test","test engineer"):
    st = "KEPT" if f in keep else ("gate-fail" if f in gate and f not in DEFN else ("definitional-exclusion" if f in DEFN else "absent (absorbed)"))
    g=gate.get(f)
    print(f"  {f:28s} -> {st}" + (f"  (senior n={g['n']}, emp={g['n_emp']}, top={g['top']:.1f}%)" if g else ""))
