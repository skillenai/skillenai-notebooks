A register has crept into AI and ML job ads over the past year. It names research only to put it in its place:

> "This is not a research role. This is not a 'play with models in a lab' role. This is a builder role."

> "Production AI shipping experience, not just research, POCs, demos, or internal experiments."

> "Not a researcher, but you can read one and tell us whether the result matters for our problem."

And, in a list headed *You Might Not Be a Fit If*: **"Your experience is limited to experimentation without production systems."**

Every one of those is a real sentence from a real US job posting. If you are a data scientist, a research engineer, or anyone whose work involves finding out whether a thing actually works, you have read a version of them and drawn a conclusion: the market has turned, research is a liability, learn to say "ship."

We went and checked. Across **62,659 US tech job postings** carrying a real description, from **8,728 employers**, the conclusion does not survive contact with the data. The register is rare, it is worth nothing in pay, and the ads writing it are asking for research anyway.

## The line is much rarer than it feels

![Share of US tech postings that disclaim research versus those that name research, evals or experimentation as the job](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/Eu4XfJq4zUE-01-who-disclaims-research.png)

| Role family | Says the job is *not* research | Names research, evals or experimentation as the job |
|---|---:|---:|
| AI Engineer | **2.7%** | **43.3%** |
| ML Engineer | 1.9% | 43.4% |
| Data Scientist | 1.0% | 32.3% |
| Research / Applied Scientist | 0.8% | 73.2% |
| Data Engineer | 0.2% | 6.4% |
| Data Analyst | **0.0%** (0 of 2,218) | 8.5% |
| Software Engineer | 0.5% | 8.1% |

An AI Engineer posting is about five times more likely than a software engineering posting to carry the disclaimer, so the impression that it clusters in AI hiring is correct. But in absolute terms it is a fringe habit: **0.7% of US tech postings** overall, and only **2.1% of employers** ever write it. Every role family here is between 16 and 88 times more likely to name research, evaluation or experimentation as part of the job than to disown it.

Three checks, because prevalence numbers are easy to inflate. Longer ads contain more of everything, so we standardised role families to a common description-length distribution: AI Engineer moves from 2.74% to 2.66%. One company can post the same boilerplate forty times, so we collapsed duplicates and also measured at the employer level. And the 439 postings carrying the register come from **179 distinct employers**, the largest being 13% of the bucket. Nobody is generating this single-handed.

## It is worth nothing

![Advertised pay effect of each phrase, raw versus compared within the same employer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/E5nL-Uj1eN8-02-what-the-words-are-worth.png)

Ads carrying the disclaimer advertise a **$205,000** median against $190,000 for everything else. A 7.9% premium. Case closed?

No. That gap is not about the job, it is about the company. The way to see this is to put a control in the model that *cannot possibly* affect pay and watch what happens to it. We used two: the phrase "equal opportunity employer" and the word "dental."

In a raw comparison, "equal opportunity employer" reads as a **9.4% pay cut**. Even with seniority, role, location, platform and ad length controlled, it still reads as **−6.0%**. That is nonsense, and it is a measurement of how much of every raw gap in job-posting data is really a difference between employers. Compare each ad against other ads *at the same company* and the placebo falls to **−0.4%** and "dental" to **+0.1%**, both indistinguishable from zero. That is a calibrated model. Here is what it says:

| Phrase in the ad | Raw gap | Same employer, same level, same role |
|---|---:|---:|
| Evaluation work (evals, eval harness, offline/model evaluation) | +15.8% | **+2.5%** (p=0.001) |
| PhD mentioned | +8.1% | **+2.8%** (p=0.02) |
| Rigorous experimentation, ablations | +10.5% | +2.1% |
| Publications, venues, research culture | +12.7% | +1.9% |
| Production-grade / production systems | +6.9% | **+1.1%** (p=0.02) |
| "Ship fast", "bias for action", "move fast" | +6.8% | **+0.3%** |
| **"This is not a research role"** | **+7.9%** | **−2.8%** (p=0.40) |
| *Placebo: "equal opportunity employer"* | *−9.4%* | *−0.4%* |

The shipping swagger prices at **zero**, and tightly: the confidence interval runs from −0.7% to +1.3%. Companies that talk that way do pay more, but the sentence does not mark a better-paid job at those companies. The anti-research line prices at zero or slightly negative; with 167 salaried ads carrying it we can say any premium is smaller than about 4%, not that it is exactly nil.

The line that *does* survive every control is the one being disparaged. **Naming evaluation work is worth +2.5% within the same employer** and beats the shipping register head-to-head by 2.1 points (p=0.03). It is not a proxy for "this is an LLM job" — add a control for mentioning LLMs or generative AI and evaluation holds at +2.5% while the control itself sits at +0.4% and is not significant. Requiring a PhD is worth **+2.8%**, not a penalty.

## The ads disclaiming research are asking for research

![Share of LLM and generative-AI postings that ask for evaluation work, with and without the disclaimer](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/09/22/e955cb79-d6bf-4b65-9c50-5facd727e73f/H6HEgM4vzkY-03-asking-for-it-anyway.png)

Here is the part that should embarrass whoever is writing these. Restricting to postings that mention LLMs or generative AI, so we are not just comparing AI jobs to everything else:

| Role family | Ads with the disclaimer | Every other ad in the role |
|---|---:|---:|
| Software Engineer | **64.0%** | 12.8% |
| ML Engineer | **56.9%** | 30.6% |
| AI Engineer | 41.4% | 40.5% |
| Data Scientist | 20.8% | 24.7% |
| **Pooled** | **53.1%** | **21.0%** |

A software engineering ad that says "this is not a research role" is **five times more likely** than a normal software engineering ad to go on and ask for eval harnesses, offline evaluation and LLM-as-a-judge.

And inside AI Engineer, the gap disappears: 41.4% versus 40.5%, p=0.88. That null is the sharper result. **Evaluation is roughly 40% of AI Engineer ads whether or not they disclaim research.** The disclaimer is not telling a candidate anything about the scope of the work, because the work is the same either way. It is describing a posture.

## There is no trade-off to make

Split postings by which registers they use at all, and the supposed dichotomy evaporates:

| The ad uses | Median advertised pay (all tech) |
|---|---:|
| Neither register | $178,100 |
| Production register only | $197,500 |
| Research / evaluation register only | $205,000 |
| **Both** | **$215,000** |

Predicted pay for one fixed job, a senior AI Engineer in California working hybrid: **$233,207** if the ad only talks about shipping, **$233,339** if it only talks about research and evaluation. A difference of $132. The top of the market is the ads that do both, at $236,511.

## A word to whoever is writing these lines

*This part is argument rather than measurement, and it is worth saying plainly.*

The register treats research, evaluation, experimentation and prototyping as tells of a candidate who cannot be trusted near production. The data says those are the parts of the job the market pays a premium for, that the companies writing the line are hiring for them anyway, and that the swagger itself is worth nothing.

That would just be a bad trade if the functions were optional. They are not. Shipping a probabilistic system without evaluation is shipping without tests. There is no other mechanism for knowing whether the thing works, whether last week's prompt change made it worse, or whether a model upgrade quietly regressed a customer-facing path. Offline evals, then online evals, against a rubric, is the closest thing this field has to a release process. A team that has screened out the people who build that capability has not trimmed a cost centre. It has removed its only instrument, and it will find out the same way everyone finds out, in production, from a customer.

The irony is sitting right there in the postings. The same ad that says *this is not a research role* asks, four paragraphs later, for an evaluation harness and someone who can judge whether a result matters. The employer wants the function. It has decided the word is a liability.

## What this means for you

- **If you are a candidate:** do not rewrite yourself out of the evaluation and experimentation work to sound production-first. The production-first register is worth, measurably, nothing. Evaluation is the strongest single line in the pay table, and the best-paying ads want both halves.
- **If you are reading an ad with this line:** treat it as a culture signal, not a scope signal. It predicts nothing about whether the job involves evaluation. Ask in the interview what their eval process is; roughly two in five AI Engineer roles have one to describe.
- **If you are writing job ads:** the sentence is costing you researchers and buying you nothing. You are not filtering for pragmatism, you are filtering out the people who would have told you the model regressed.
- **If you lead an AI product team:** staff evaluation deliberately. The market already prices it above the swagger, which is usually a sign it is scarce.

## Methodology

62,659 US postings from the Skillenai enriched job index whose role matches an AI, ML, data or software engineering family and which contain real description text. Postings with empty descriptions are excluded up front — on some applicant-tracking platforms the description never lands, and those documents would otherwise sit in every denominator and understate every figure.

The registers are families of regular expressions over cleaned posting prose. The phrasings were discovered from the corpus first — sentences containing research, papers, academia, prototypes or notebooks near a negation were mined and the recurring constructions written up — rather than guessed from a word list. Precision was audited by reading sampled matches. A "PhD not required" pattern was tested and dropped: most of its matches turned out to be inclusive rather than dismissive.

Pay uses 24,445 salaried postings across 3,788 employers. Pay units are normalised before pooling, role titles are merged into families with seniority words stripped, and the reported model holds employer, seniority, role family and description-length quintile constant with standard errors clustered by employer. Confidence intervals are 95%.

What this cannot tell you: whether the register is spreading — only two quarters of reliably source-dated postings clear a usable sample, so no trend is fitted. Nor anything about equity, since these are advertised base ranges and the companies most fluent in shipping swagger are disproportionately the ones that pay in stock. And these are advertisements, not hires.

A related finding worth holding alongside this one: an [earlier analysis of the LLM-eval landscape](https://github.com/skillenai/skillenai-notebooks/tree/master/llm-eval-landscape) found that no named evaluation *framework* cracks 1% adoption in job postings. Employers name the evaluation **function** constantly, and the evaluation **products** almost never. The job is established; the tooling is not.

[Full methodology, data and code](https://github.com/skillenai/skillenai-notebooks/tree/master/not-a-research-role)
