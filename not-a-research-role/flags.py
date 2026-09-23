"""Rhetorical-register flags for job-posting text.
Each register is a LIST of regex strings so per-pattern hit counts can be audited."""
import re

PATS = {
# ---- 1. explicitly subordinates research / papers / prototypes / notebooks
"anti_research": [
 r"\bthis is not (?:a |an )?(?:pure |purely |traditional |academic |theoretical )?research\b",
 r"\bnot (?:a |an )?(?:pure |purely |traditional |academic |theoretical )?research[- ]?(?:only |focused |oriented |heavy )?(?:role|position|job|team|lab|laboratory|organi[sz]ation|project|gig|environment|function|group)\b",
 r"\bnot (?:just|only|merely|purely|solely) (?:doing |about |a )?research\b",
 r"\bnot (?:just|only|merely|solely) (?:about |writing |publishing |publish |producing )?(?:research )?papers\b",
 r"\bresearch for research'?s? sake\b",
 r"\bivory tower\b",
 r"\bpublish or perish\b",
 r"\bnot (?:a |an )?(?:academic|science) (?:role|position|exercise|project|environment)\b",
 r"\bpapers? (?:don'?t|do not|won'?t) ship\b",
 r"\bwe (?:don'?t|do not) (?:just )?(?:write|publish) papers\b",
 r"\brather than (?:doing |pure )?research\b",
 r"\bmore than (?:just )?(?:a )?(?:research|papers|prototypes)\b",
 r"\b(?:beyond|past|out of) (?:the )?(?:notebook|notebooks|jupyter)\b",
 r"\bnot (?:just|only) (?:in |writing )?(?:a |the )?(?:notebook|notebooks|jupyter)\b",
 r"\bnot (?:a |an )?(?:prompt engineering|science project)\b",
 r"\bnot (?:a |an )?researcher\b",
 r"\bnot (?:just|only|merely) (?:prototypes?|demos?|pocs?|proofs? of concept|research demos?)\b",
 r"\bresearch without production\b",
 r"\bengineering role,? not a research\b",
 r"\bplay with models\b",
],
# reported separately: small n and mixed precision (inclusive "without a PhD" excluded)
"phd_not_needed": [
 r"\b(?:ph\.?\s?d\.?|doctorate) (?:is )?not (?:required|necessary|needed)\b",
 r"\bno (?:ph\.?\s?d\.?|doctorate) (?:is )?(?:required|necessary|needed)\b",
 r"\b(?:don'?t|do not) need (?:a |an )?(?:ph\.?\s?d\.?|doctorate)\b",
],
# ---- 2. research/prototype -> production pipeline framing (neutral-to-subordinating)
"pipeline": [
 r"\b(?:from )?(?:research|prototype|prototypes|poc|pocs|proofs?[- ]of[- ]concept|pilot|pilots|demo|demos|notebook|notebooks|lab|idea|ideas|experiments?)\s+(?:in)?to production\b",
 r"\bproduction[a-z]*i[sz]ation\b", r"\bproduction[a-z]*i[sz]e[ds]?\b", r"\bproductioni[sz]ing\b",
 r"\bresearch (?:in)?to (?:real|product|reality)\b",
 r"\btranslat(?:e|ing) research\b", r"\bfrom the lab to\b",
 r"\bbridge the gap between research\b",
],
# ---- 3. production-primacy register that never names research
"ship_register": [
 r"\bship(?:s|ped|ping)?\s+(?:fast|quickly|early|often|daily|weekly|production|real|working|code|features?|products?)\b",
 r"\bbias (?:for|toward|towards|to) (?:shipping|action|delivery)\b",
 r"\b(?:actually|love to|loves to|like to) ship\b", r"\bship it\b", r"\bshipping mentality\b",
 r"\bmove fast\b", r"\broll up (?:your|their) sleeves\b", r"\bget (?:your|their) hands dirty\b",
 r"\bscrappy\b", r"\bsense of urgency\b", r"\bget things done\b", r"\bbuilder'?s? mentality\b",
 r"\bproduction[- ]first\b", r"\bbuilder role\b",
],
"prod_grade": [
 r"\bproduction[- ](?:grade|ready|quality|level)\b", r"\bproduction systems?\b",
 r"\bin production at scale\b", r"\brunning in production\b",
 r"\bdeploy(?:ed|ing)? to production\b", r"\breal[- ]world (?:impact|systems|applications)\b",
],
# ---- 4. research explicitly valued
"publications": [
 r"\bpublish(?:ed|ing)? (?:in |at |research|papers|your work|work in|work at)\b",
 r"\bpublications?\b", r"\bpeer[- ]review(?:ed)?\b", r"\bfirst[- ]author\b",
 r"\bpublication record\b", r"\bh[- ]index\b", r"\bpublished papers\b",
],
"venues": [r"\b(?:neurips|icml|iclr|cvpr|eccv|iccv|emnlp|naacl|kdd|aaai|ijcai|siggraph|aistats|colm|interspeech)\b"],
"research_culture": [
 r"\bresearch[- ](?:driven|first|culture|agenda|roadmap|mindset|minded|oriented)\b",
 r"\b(?:novel|original|fundamental|open[- ]ended|frontier|cutting[- ]edge|applied) research\b",
 r"\bwe publish\b", r"\bresearch questions?\b", r"\bresearch problems?\b", r"\bopen problems?\b",
],
"experimentation": [
 r"\b(?:rigorous|systematic|careful|disciplined) experimentation\b",
 r"\bexperimental design\b", r"\bdesign(?:ing)? (?:and (?:running|executing) )?experiments\b",
 r"\brun(?:ning|s)? experiments\b", r"\bhypothes[ie]s[- ]driven\b", r"\bablations?\b",
 r"\bscientific (?:method|rigor|rigour|approach)\b", r"\b(?:experimental|research) rigor(?:ous)?\b",
 r"\bdesign experiments\b", r"\bexperiment(?:al)? framework\b",
],
"evals": [
 r"\bevals\b", r"\beval (?:harness|suite|framework|sets?|pipelines?|infrastructure|metrics|driven)\b",
 r"\b(?:model|llm|offline|online|automated|human|systematic|rigorous) evaluation\b",
 r"\bevaluation (?:framework|metrics|harness|suite|pipelines?|sets?|criteria|methodolog)\w*\b",
 r"\bllm[- ]as[- ]a?[- ]?judge\b", r"\beval(?:uation)? driven development\b",
],
"stats_rigor": [
 r"\bstatistical(?:ly)? (?:significan|rigor|method|model|inference|analysis)\w*\b",
 r"\bcausal inference\b", r"\bcontrolled experiments?\b", r"\bpower analysis\b",
 r"\ba/?b test(?:ing|s|ed)?\b", r"\bsplit test(?:ing|s)?\b", r"\bexperimentation platform\b",
],
"phd": [r"\bph\.?\s?d\.?s?\b", r"\bdoctorate\b", r"\bdoctoral\b"],
# calibration placebos: boilerplate that cannot plausibly change advertised pay
"placebo_eoe":  [r"\bequal opportunity employer\b"],
"placebo_dent": [r"\bdental\b"],
# "is this an LLM/GenAI job at all" control
"llm": [r"\b(?:llm|llms|large language model|generative ai|genai|foundation model|gpt-?4|claude|transformer|rag\b|fine[- ]tun)"],
}

# STRICT = the subset of anti_research that actually NAMES research/papers/academia/notebooks.
# The remainder of anti_research is "not just prototypes / demos / PoCs", which is in-register
# but never says the word. Headline prevalence uses STRICT; the broad variant is the upper bound.
PATS["anti_research_strict"] = [p for p in PATS["anti_research"]
    if not any(w in p for w in ("prototypes?|demos?", "production[- ]first"))]
PAT = {k: re.compile("|".join(v), re.I) for k, v in PATS.items()}

def add_flags(df, col="text"):
    t = df[col].fillna("")
    for k, p in PAT.items():
        df["f_" + k] = t.str.contains(p, regex=True)
    df["f_research_any"] = df["f_publications"] | df["f_venues"] | df["f_research_culture"]
    df["f_research_positive"] = df["f_research_any"] | df["f_experimentation"] | df["f_evals"]
    df["f_prod_any"]     = df["f_ship_register"] | df["f_prod_grade"]
    df["f_rigor_any"]    = df["f_experimentation"] | df["f_evals"] | df["f_stats_rigor"]
    return df

def pattern_hits(texts, key):
    import collections
    c = collections.Counter()
    for s in texts:
        for sp in PATS[key]:
            if re.search(sp, s, re.I): c[sp] += 1
    return c
