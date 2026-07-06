import pandas as pd, json, re, math
fed = pd.read_parquet("federal_tech_hf.parquet")
fed['title_l'] = fed.title.str.lower()

def load_priv(f):
    return [(h.get("extractedText") or "") for h in json.load(open(f))]
PRIV = {"DS": load_priv("private_ds.json"), "SWE": load_priv("private_swe.json"), "SEC": load_priv("private_sec.json")}

# Federal role subsets (from HF corpus)
def fedtxt(mask): return list(fed[mask].duties)
FED = {
 "DS": fedtxt(fed.title_l.str.contains("data scientist|data science") | fed.series.isin(["1560"])),
 "SWE": fedtxt((fed.series.isin(["2210","1550"])) & fed.title_l.str.contains(
     "software|developer|programmer|application|appsw|full stack|web ")),
 "SEC": fedtxt(fed.title_l.str.contains("cyber|security|infosec|information security|information assurance")),
}

SKILLS = {
 # languages
 "Python": r"\bpython\b", "Java": r"\bjava\b(?!script)", "JavaScript": r"\bjavascript\b",
 "TypeScript": r"\btypescript\b", "Go (Golang)": r"\bgolang\b|\bgo\b programming", "C++": r"c\+\+",
 "COBOL": r"\bcobol\b", "ColdFusion": r"coldfusion", "Visual Basic": r"visual basic|\bvb\.net\b",
 "PL/SQL": r"pl/sql", "PHP": r"\bphp\b", "Ruby": r"\bruby\b",
 # web
 "React": r"\breact\b", "Angular": r"\bangular\b", "jQuery": r"jquery", "Node.js": r"node\.?js",
 "HTML/CSS": r"\bhtml\b|\bcss\b",
 # cloud/infra
 "AWS": r"\baws\b|amazon web services", "Azure": r"\bazure\b", "GCP": r"\bgcp\b|google cloud",
 "Kubernetes": r"kubernetes|k8s", "Docker": r"\bdocker\b", "Terraform": r"terraform",
 "CI/CD": r"ci/cd|continuous integration", "microservices": r"microservice",
 "Linux": r"\blinux\b", "cloud (any)": r"\bcloud\b",
 # data/ML
 "SQL": r"\bsql\b", "Spark": r"\bspark\b", "pandas/NumPy": r"\bpandas\b|\bnumpy\b",
 "scikit-learn": r"scikit|sklearn", "TensorFlow/PyTorch": r"tensorflow|pytorch",
 "machine learning": r"machine learning|\bml\b", "LLM / GenAI": r"\bllm\b|large language model|generative ai|\bgenai\b",
 "A/B testing": r"a/b test|experimentation", "causal inference": r"causal infer",
 "data pipelines/ETL": r"data pipeline|\betl\b", "SAS": r"\bsas\b", "R (stats)": r"\bR\b programming|\bin R\b|using R\b|\bR/SAS\b",
 "Tableau/Power BI": r"tableau|power ?bi",
 # security
 "penetration testing": r"penetration test|pen[- ]?test", "threat modeling": r"threat model",
 "SIEM": r"\bsiem\b", "vulnerability mgmt": r"vulnerabilit", "incident response": r"incident response",
 "SOC / SecOps": r"\bsoc\b|security operations", "NIST": r"\bnist\b", "RMF": r"\brmf\b|risk management framework",
 "FISMA/FedRAMP": r"fisma|fedramp", "ATO / A&A": r"authorization to operate|assessment and authorization|\bato\b",
 "DevSecOps": r"devsecops", "zero trust": r"zero trust",
 # practices / federal
 "Agile/Scrum": r"\bagile\b|\bscrum\b", "security clearance": r"security clearance|clearance",
 "SDLC": r"\bsdlc\b|software development life ?cycle", "configuration mgmt": r"configuration management",
}

def rate(texts, pat):
    rx = re.compile(pat, re.I); n = len(texts)
    return (sum(1 for t in texts if rx.search(t)) / n) if n else 0.0

def chi2_p(a, b, c, d):
    n = a+b+c+d
    if min(a+b, c+d, a+c, b+d) == 0: return 1.0
    obs = [a, b, c, d]
    exp = [(a+b)*(a+c)/n, (a+b)*(b+d)/n, (c+d)*(a+c)/n, (c+d)*(b+d)/n]
    chi = sum((o-e)**2/e for o, e in zip(obs, exp) if e > 0)
    return math.erfc(math.sqrt(chi/2))

out = {}
for role in ["DS", "SWE", "SEC"]:
    f, p = FED[role], PRIV[role]
    Nf, Np = len(f), len(p)
    rows = []
    m = len(SKILLS)
    for sk, pat in SKILLS.items():
        pf, pp = rate(f, pat), rate(p, pat)
        a = round(pf*Nf); c = round(pp*Np)
        pval = chi2_p(a, Nf-a, c, Np-c)
        rows.append((sk, pf, pp, pval, pval < 0.05/m))
    out[role] = {"Nf": Nf, "Np": Np, "rows": rows}
    print("\n" + "="*74)
    print("%s | FEDERAL(HF) N=%d  vs  PRIVATE(index) N=%d | Bonferroni=%.4g" % (role, Nf, Np, 0.05/m))
    print("  %-24s %7s %8s %8s  sig" % ("skill", "fed%", "priv%", "ratio"))
    print("  -- private-leaning --")
    for sk, pf, pp, pval, sig in sorted(rows, key=lambda x: (x[1]+.001)/(x[2]+.001))[:12]:
        print("  %-24s %6.0f%% %7.0f%%  p/f %4.1fx  %s" % (sk, 100*pf, 100*pp, (pp+.001)/(pf+.001), "*" if sig else ""))
    print("  -- federal-leaning --")
    for sk, pf, pp, pval, sig in sorted(rows, key=lambda x: (x[2]+.001)/(x[1]+.001))[:10]:
        print("  %-24s %6.0f%% %7.0f%%  f/p %4.1fx  %s" % (sk, 100*pf, 100*pp, (pf+.001)/(pp+.001), "*" if sig else ""))
json.dump({r: {"Nf": out[r]["Nf"], "Np": out[r]["Np"],
               "rows": [[s, round(pf, 4), round(pp, 4), sig] for s, pf, pp, _, sig in out[r]["rows"]]}
           for r in out}, open("hf_vs_private.json", "w"), indent=1)
