<!--
BLOG DRAFT — HELD for joint Skillenai × Live Data review (do not publish until Alex signs off).
Intended byline: Skillenai AI Analyst. Category: insights-and-analytics.
Suggested tags: data science, data scientist, government tech, careers, machine learning engineer, labor market
Cover image: 03_flows_in_out.png
When publishing: upload the three figures to the Skillenai media store, swap the relative
image links below for the returned media.skillenai.com URLs, and switch the notebooks link to /tree/master/.
-->

# Federal Data Scientists Rarely Come From — or Go To — Big Tech

A federal data scientist is more likely to have studied **epidemiology** than a private one — and far more likely to end up at **Booz Allen** than at **Google**. We looked at the people, not just the job posts, and found two data-science worlds that barely trade members.

Two earlier pieces looked at federal tech from the employer's side: the [pay-and-pension bargain](https://skillenai.com/2026/06/23/the-federal-tech-bargain) and the [skills wall](https://skillenai.com/2026/07/07/same-job-title-different-job-inside-federal-vs-private-tech-hiring) — where, under identical titles, a federal Data Scientist posting is *statistics-and-reporting* and a private one is *code-experiment-deploy*. Both left the same question open: **is that because the two sectors hire fundamentally different people — and can those people even move between them?**

This time we answered it from the **supply** side — using worker profile histories (job history + education) instead of job postings, via [Live Data (workforce.ai)](https://workforce.ai). The short version: the skills wall is real because the *people* and their *career circuits* are different, and the door between federal and frontier-tech data science is shut in both directions.

## Two weakly-connected worlds

![Where federal data scientists come from and where they go](03_flows_in_out.png)

Follow federal data scientists in and out of government:

- **In:** of those who joined mid-career, about **46% came from academia** and **32% from older-economy private industry** (Micron, Illumina, Roche, Verizon, Target, USAA, insurance and telecom firms). Exactly **one in 76** came from Big Tech or a frontier-AI lab. The most "tech" origin in the entire sample was eBay.
- **Out:** across **1,181** federal data scientists, the next job after leaving is **another federal agency 76%** of the time, and a **cleared contractor or consultancy** (Booz Allen, MITRE, Deloitte) another **18%**. Exactly **4 of 1,181** — **0.3%** — went to Google.

There *is* a pipeline into federal data science. It just runs through universities and the legacy economy, not through the companies building modern machine learning.

## Different people

![Federal vs private data scientist fields of study](01_education_funnels.png)

Read what the two populations studied and the funnels split apart:

| Field of study | Federal DS | Private-tech DS |
|---|---:|---:|
| Statistics | 4.4% | **9.4%** |
| Computer Science | 6.7% | 7.2% |
| Epidemiology | **5.2%** | 0.3% |
| Psychology | **3.6%** | 0.8% |
| Biostatistics | 3.2% | 1.5% |
| Economics | 4.4% | 5.3% |
| Mechanical / Industrial Engineering | ~0% | 3.9% combined |

*(Share of each cohort holding a degree in the field; people can hold more than one, so columns don't sum to 100. Federal N=252, private N=7,683.)*

The surprise is what's **not** the difference: Computer Science is essentially tied. Federal data scientists aren't CS-poor. What sets them apart is a heavy **domain- and social-science tail** — epidemiology, psychology, biology — while private data scientists sit on a broader **quant-and-engineering** base, including a mechanical/industrial/chemical-engineering feeder that has no federal counterpart. The federal data scientist is often a subject-matter expert who *took up* data science; the private one is a technical specialist who trained for it.

## Different careers

![What federal data scientists have actually done](02_title_history.png)

Their work histories say the same thing. Of 100 federal data scientists, the share who have **ever held a title containing**:

| Role | Share |
|---|---:|
| Researcher / Fellow | 64% |
| Analyst | 48% |
| Statistician | 25% |
| Machine Learning / AI | **13%** |
| Software / Developer | **11%** |

These are researchers and analysts by trade, not system builders — exactly what the postings implied when federal listings named "machine learning" as often as private ones yet rarely asked for Python, experimentation, or MLOps. The lineage is even stamped into their current titles, which read `Statistician (Data Scientist)`, `Health Scientist (Data Scientist)`, and `Mathematical Statistician (Data Scientist)`.

## What this means for your career

**If you're a federal data scientist eyeing private tech:** your résumé likely reads *domain scientist / statistician / analyst*, and the frontier-tech market hires for *engineering and experimentation*. The move is a retraining project, not just a résumé refresh — and the near-total absence of this path in the data is the honest measure of how hard it is.

**If you're at a frontier-tech firm considering federal service:** almost no one has done it, which cuts both ways. The culture and tooling gap is real, but so is the scarcity — if the mission appeals, you'd be rare.

**If you're a hiring leader in government:** closing the pay gap alone won't conjure a modern ML-engineering workforce. The talent government can realistically attract is the analyst/researcher lineage it already draws — a different job architecture from the one frontier tech runs on. That's the deeper reason the roles are hard to fill, and why the people who leave are so hard to replace: there was never a frontier-tech pipeline to backfill from.

## Methodology

Supply-side profile data from Live Data (workforce.ai): data scientists at ten federal agencies (Veterans Affairs, Defense, CDC, NIH, IRS, CMS, Federal Reserve, Treasury, NASA, Census) versus nine private tech firms (Google, Meta, Amazon, Microsoft, Apple, Netflix, Uber, Airbnb, Salesforce). Education distributions cover 252 federal and 7,683 private data scientists; career-path flows cover 1,181 federal data scientists; origin classification is a hand-checked 100-profile sample.

Caveats: the profile schema exposes education and job history, **not** the free-text LinkedIn "Skills" field — so education, titles, and movement are a proxy for skill, not a direct read of listed skills. LinkedIn under-captures career civil servants and can't cleanly separate them from on-site contractors. The federal agency set is health/benefits-heavy, which shapes the specific domains in the tail. Private-tech flow shares are floors (long-tail destinations are truncated in the aggregate).

*[Full methodology, data, and figures](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-vs-tech-data-scientists) · A Skillenai × Live Data analysis.*
