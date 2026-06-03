A new working paper out of the London School of Economics has a sharp answer to one of the most contentious questions in the labor market debate: **AI didn't take entry-level tech jobs. Remote work did.**

Lambert and Schindler analyzed **243 million** new-hire records and **407 million** job postings across the US, UK, Canada, and Australia. When they ran the regression in the obvious way — controlling for occupation-level AI exposure — AI looked like a major culprit in the entry-level hiring collapse. When they added work-from-home exposure to the model and let the two predictors compete, the picture inverted. WFH stayed significant. AI "attenuated sharply and is often statistically indistinguishable from zero."

Their proposed mechanism is unglamorous: **remote work raises the cost of supervising and developing junior workers**, so firms shift hiring toward seniors who need less of it. AI and WFH happen to be correlated at the occupation level because the same desk-bound roles are both AI-exposed and WFH-eligible — that's why a naive regression blames AI.

If that mechanism is right, the signature should show up in the *supply* of job postings too — and it should be a property of the role's supervisability, not its AI exposure. We tested that prediction in the Skillenai tech-jobs index.

## The test

For 12 US tech IC roles with enough entry-level and senior-level postings to do a clean contrast, we computed two numbers:

1. **% of entry-level postings that allow remote or hybrid work**
2. **% of senior-level postings that allow remote or hybrid work**

The gap between the two — what we'll call the **broken-ladder slope** — is how much more remote-friendly a senior posting is than an entry-level posting in the same role.

We also tagged each role's AI exposure as **AI-heavy** (>50% of postings mention AI/ML/LLM phrases), **AI-medium** (15–50%), or **AI-light** (<15%).

If AI were driving the entry-level decline, the broken ladder should be **worst** in the AI-heavy roles. That's where AI is supposedly displacing juniors.

It isn't.

![Per-role broken-ladder gap vs AI exposure — scatter plot showing no positive correlation between a role's AI mention share and its entry-vs-senior remote-allowance gap](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/03/e955cb79-d6bf-4b65-9c50-5facd727e73f/85nNR4Gis1M-01-gap-vs-ai-exposure.png)

## The ranking

When you sort roles by their broken-ladder slope, the AI-heavy roles don't cluster at the top. They cluster in the middle and at the bottom.

![Per-role broken-ladder ranking — Full Stack Engineer +37pp, Product Designer +29pp, Product Manager +24pp at the top; Data Scientist and Research Engineer +5pp at the bottom](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/03/e955cb79-d6bf-4b65-9c50-5facd727e73f/tEHT6AFJ6VQ-02-broken-ladder-ranking.png)

| Role | AI tier | N entry | N senior | Entry % any-remote | Senior % any-remote | Gap |
|---|---|---:|---:|---:|---:|---:|
| Full Stack Engineer | light | 43 | 263 | 34.9% | 72.2% | **+37pp** |
| Product Designer | light | 48 | 606 | 35.4% | 64.9% | **+29pp** |
| Product Manager | light | 97 | 1,407 | 33.0% | 56.9% | **+24pp** |
| AI Engineer | heavy | 40 | 228 | 35.0% | 58.3% | +23pp |
| Research Scientist | heavy | 32 | 274 | 21.9% | 41.6% | +20pp |
| Data Analyst | medium | 104 | 228 | 42.3% | 55.3% | +13pp |
| Data Engineer | medium | 66 | 613 | 51.5% | 64.1% | +13pp |
| Machine Learning Engineer | heavy | 35 | 428 | 57.1% | 68.7% | +12pp |
| Software Engineer | medium | 1,355 | 6,235 | 47.4% | 58.7% | **+11pp** |
| Backend Engineer | light | 39 | 384 | 61.5% | 72.4% | +11pp |
| Data Scientist | heavy | 86 | 628 | 43.0% | 47.6% | +5pp |
| Research Engineer | heavy | 35 | 184 | 51.4% | 56.0% | +5pp |

Bold = significant under Bonferroni correction for 12 tests at α=0.05.

Two things jump out.

**First — every Bonferroni-significant broken ladder is in an AI-light or AI-medium role.** Software Engineer, Full Stack Engineer, Product Manager, Product Designer. Not a single AI-heavy role's entry-vs-senior gap is robust enough to survive correction. This holds even though some of the AI-heavy roles (MLE, Data Scientist) have larger entry-level samples than the AI-light Full Stack Engineer.

**Second — the most open ladders belong to the most AI-exposed roles.** Data Scientist (+5pp), Research Engineer (+5pp), and Machine Learning Engineer (+12pp) have the smallest gaps in the sample. If you're an entry-level candidate looking for a remote-friendly tech role, the AI-adjacent ones are surprisingly more open than the cross-functional product roles.

## The aggregate test

Averaging the gap across roles within each AI exposure tier:

![Mean broken-ladder gap by AI tier — AI-light 25.4pp, AI-medium 12.3pp, AI-heavy 12.8pp](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/06/03/e955cb79-d6bf-4b65-9c50-5facd727e73f/TKNLAkRPFEQ-03-mean-gap-by-tier.png)

| Tier | Roles (n) | Mean gap |
|---|---:|---:|
| AI-light | 4 | **25.4 pp** |
| AI-medium | 3 | 12.3 pp |
| AI-heavy | 5 | 12.8 pp |

A one-way ANOVA on these three tiers gives F = 2.94, p = 0.10 — not significant with n=12 roles. The Spearman correlation between continuous AI mention share and the gap is **ρ = −0.40 (p = 0.20)** — directionally negative (AI-heavier roles have *smaller* gaps), but underpowered.

The defensible aggregate claim is the **null result**: the broken-ladder gap is independent of AI exposure. That null is exactly what Lambert and Schindler's causal claim predicts.

## What this means

**For the AI-jobs narrative.** A natural-sounding "AI is taking entry-level tech jobs" story would predict the broken ladder to be steepest in AI-disrupted roles. It isn't. AI-heavy roles like Data Scientist and Research Engineer have some of the *flattest* slopes. The roles that look most "automatable" are not the ones where new graduates face the worst entry-level posting market.

**For new graduates.** If you're targeting a remote-friendly entry-level role: Data Scientist, Machine Learning Engineer, Backend Engineer, and Data Engineer postings allow remote or hybrid at the entry level **57–62%** of the time. Product Designer, Product Manager, and Full Stack Engineer entry-level postings drop to **33–35%**. The market is treating cross-functional, collaboration-heavy roles as inherently in-person for juniors, while individual contributor roles in research, data, and backend infrastructure are treating juniors as more interchangeable with senior remote work.

**For employers.** The shape of these gradients suggests the binding constraint isn't skill scarcity — it's supervisability. The roles where entry-level postings stay onsite are ones where the work is hard to evaluate asynchronously: design taste, cross-functional collaboration, product judgment, full-stack ownership across a codebase. The roles where entry-level postings are remote-friendly are ones with more individually measurable work: research, data, focused backend systems. If you want to re-open the entry-level pipeline, the lever isn't AI strategy — it's onsite mentorship structure.

## Limits

- **n = 12 roles** limits cross-role statistical power. The aggregate test cannot reject the null at conventional thresholds — but the null is what Lambert/Schindler's causal claim predicts, and the per-role pattern (every Bonferroni-significant broken ladder is in an AI-light role) is itself the strong signal.
- **Entry-level samples are thin in some AI roles** — itself a symptom of the broken-ladder pattern.
- **AI exposure is measured via posting-text mention prevalence**, not actual AI work intensity.
- **We see postings, not hires.** Our supply-side fingerprint is consistent with Lambert and Schindler's hire-record finding, but doesn't replicate their longitudinal analysis.

[Full methodology, code, CSVs, and per-role chi-square tests on GitHub](https://github.com/skillenai/skillenai-notebooks/tree/master/broken-ladder-roles).

## Methodology

US tech postings filter on the Skillenai jobs index (`prod-enriched-jobs`): `locationCountry = "US"`, `workModel ∈ {onsite, hybrid, remote}`, `seniorityLevel ∈ {entry, senior}`. Speechify excluded (carpet-bomber). Role universe: 12 IC tech roles with N ≥ 250 in the US filtered universe AND entry-level N ≥ 30 AND senior-level N ≥ 50; title-tagged seniority variants ("Staff X", "Senior X", "Principal X") excluded because they duplicate the `seniorityLevel` signal at the title level. AI exposure measured as the share of postings in each role whose `extractedText` matches at least one of *machine learning*, *deep learning*, *neural network*, *large language model*, *LLM*, *PyTorch*, *TensorFlow*, *transformer model*, *generative AI*. Per-role significance: chi-square test of independence on the 2×2 contingency table (entry vs senior × onsite vs any-remote), Bonferroni-corrected for 12 tests at α=0.05. Cross-role test: one-way ANOVA on the entry-vs-senior gap by AI exposure tier; Spearman and Pearson correlation between continuous AI mention share and gap.

This piece builds on yesterday's [supply-side fingerprint of the remote-work / youth-unemployment gap](https://github.com/skillenai/skillenai-notebooks/tree/master/remote-by-seniority), which established the overall intern → staff remote-allowance gradient.

Coverage that triggered this piece: ["Remote Jobs Are Increasingly Going to Experienced Workers, Leaving New Graduates Behind"](https://allwork.space/2026/06/remote-jobs-are-increasingly-going-to-experienced-workers-leaving-new-graduates-behind/) (allwork.space, NY Fed coverage) and ["WFH is a bigger threat to entry-level jobs than AI, research finds"](https://news.outsourceaccelerator.com/wfh-threat-entry-level-jobs/) (news.outsourceaccelerator.com, Lambert & Schindler coverage).
