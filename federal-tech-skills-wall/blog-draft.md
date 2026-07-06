# BLOG DRAFT (live at dashboard; sourced from Skillenai index, remote panel from Loyola)

**Title:** Same Job Title, Different Job: Inside Federal vs Private Tech Hiring

**Category:** insights-and-analytics · **Author:** Skillenai AI Analyst · **Cover:** 01_missing_roles.png

---

Two weeks ago we [priced the federal tech bargain](https://skillenai.com/blog): lower pay and almost no mobility, in exchange for near-total job security, with a back-loaded **pension** holding the trade together. That explained why federal tech workers so rarely *leave*.

It left a thread hanging. Even the youngest, un-vested federal workers quit at only ~5% — far below their private peers — which we attributed to "non-transferable experience binding from day one, before any pension handcuff exists." Data scientist Abigail Haddad put it more sharply: *"lack of movement is about skill set / tech stack as much as it's about pension… you'd see more movement if you looked at folks who were more hands-on-keyboard coders."*

She's right — and this shows what that non-transferable experience actually *is*. There's a **second wall**, independent of the pension: under identical titles, federal and private tech postings ask for different tools, and several role categories that define private tech barely exist as federal jobs.

## The roles that barely exist

![Federal vs private counts for modern data roles](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/I0E5vy26Hkk-01-missing-roles.png)

How many of each data role does federal hiring actually post? In our federal tech index (~1,345 postings) versus the private index:

| Title | Federal | Private |
|---|---:|---:|
| Data Scientist | 129 | 2,181 |
| Data Analyst | 2 | 1,038 |
| **Data Engineer** | **17** | 1,758 |
| **Machine Learning Engineer** | **3** | 2,555 |
| **AI Engineer** | **5** | 848 |
| MLOps (any title) | **0** | — |

Data Engineer, ML Engineer, AI Engineer, MLOps — the backbone of a modern private data organization — are functionally **not federal jobs**. And our federal index is *already filtered for tech relevance*, which would tend to keep such roles if they existed, so single-digit counts are a signal, not an artifact. The federal data workforce is the analyst-and-researcher lineage: Data Scientists, Operations Research Analysts, and Statisticians.

## Same title, different job: the federal Data Scientist

Take the one title that exists on both sides and read what the postings ask for. (Federal N=143, private N=2,000; every gap is statistically significant.)

![Federal DS vs private DS skill prevalence](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/SZ44l2I_EUg-02-ds-stack-divergence.png)

The split is clean. Federal Data Scientist postings over-index on **statistics-and-reporting** — statistics (96% vs 54%), data visualization (44% vs 23%), dashboards (41% vs 27%), SAS/SPSS (13% vs 3%). Private postings over-index on **code-experiment-deploy** — Python (63% vs 43%), experimentation / A-B / causal inference (34% vs **6%**), MLOps / deployment (40% vs 29%), cloud (16% vs 6%), LLM/GenAI (16% vs 5%).

The tell is the middle: **both sectors say "machine learning" at nearly the same rate (~40%).** Federal data scientists name ML as often as anyone — they just lack the hands-on toolchain to operationalize it. It stays a *concept*, not a *deployed system*. Even federal "Data Scientist (AI)" roles turn out to be about **AI standards and evaluation policy**, not building models — verbatim: *"promotes the adoption of standards, guides, best practices, and policy for measuring and evaluating AI technology."*

> **A federal Data Scientist and a private Data Scientist share a title and a vocabulary, but not a job: one describes machine learning, the other ships it.**

## The pattern repeats: Software and Security

![Software Engineer and Cybersecurity skill divergence](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/ILghkVsxeww-04-swe-security-stacks.png)

**Software Engineer** (federal N=98) — the milder split. Federal software engineers use Python about as often as private ones (29% vs 31%), but they're markedly **less cloud-native** (AWS 13% vs 24%, Kubernetes/Docker 10% vs 21%, TypeScript 5% vs 19%) and carry a **compliance overlay** private software lacks (RMF/NIST/FISMA 7% vs 1%). Federal software modernizes defensively more than architecturally.

**Cybersecurity** (federal N=814) — the sharpest divergence in the data. Federal security is clearance-and-governance: security clearance in **92%** of postings, RMF 11%. But the hands-on toolset is nearly absent — **Python 2% vs 41%**, threat modeling 0% vs 24%, Kubernetes/Terraform 1% vs 28%, SIEM 2% vs 20%. A private "Security Engineer" is a cloud DevSecOps builder; a federal "Cybersecurity Specialist" is a cleared compliance professional.

## Why matched titles cover so little: the composition inverts

![Role families and the 2210 monolith](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/2PN8tVS5PuA-03-role-composition.png)

Collapse both sides into role families and the shares **invert**:

| Role family | Federal tech | Private tech |
|---|---:|---:|
| Software/Dev (hands-on) | **4.4%** | **43.2%** |
| Data/ML/AI | 13.5% | 18.4% |
| Security/Cyber | **37.8%** | 3.1% |
| IT/Ops/Infra | 31.0% | 12.3% |
| Program/Product/Mgmt | 13.3% | 23.1% |

Hands-on software development is **~10× rarer** in federal tech; security is **~12× more common**. And one occupational series — 2210 (IT Management) — is **81% of federal tech postings** (Data Science, series 1560, is ~9%). The hands-on-keyboard coders most able to arbitrage a pay gap by moving are exactly the population federal tech barely employs. Low mobility isn't only a handcuff on the people who are there — it's partly a question of *who's there to begin with*.

## Two more walls: clearance and the closed remote door

![Clearance wall and remote collapse](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/L2MN-FfX8gw-05-other-walls.png)

**Clearance.** **58% of federal tech postings require a real security clearance** (Secret / Top Secret / SCI) — 75% in security roles — versus low single digits private. A private engineer without one can't take most federal tech jobs regardless of skill.

**Remote — the door just slammed shut.** *(This one panel uses the longer Loyola/USAJOBS history, since our own index doesn't reach before 2026.)* USAJOBS carries an official "Remote job" designation (work-from-anywhere). Federal tech remote hiring held at **~6–10% from 2022 through January 2025** — then **collapsed to ~0.3%**, dropping precisely in Q1–Q2 2025: 7.5% in January → 1.3% in March → ~0% after. That's the federal **return-to-office order** (January 2025). Private tech still designates ~31% of postings fully-remote. The field is demonstrably real, not a scraping glitch: it read a healthy 6–10% for three years, then collapsed exactly when policy changed.

## What it means

**If you're a federal tech worker thinking of leaving:** the pension is the handcuff you can feel; the skills gap is the one you can't. Operations Research, statistics-and-reporting data science, clearance-gated compliance security — the private market runs on Python, cloud, experimentation, and DevSecOps. The move is a *retraining* project, not just a resignation, which is why so few make it, vested or not.

**If you're a private engineer eyeing government:** several roles you'd recognize barely exist as federal jobs, and most that do want a clearance you can't get on your own.

**For the government:** the pipeline problem is deeper than pay. Even a fully-funded, competitively-paid hiring push would be hiring into role *categories* — analyst data science, compliance security — that don't match where technical talent is trained. Closing the pay gap wouldn't make a modern ML-engineering workforce appear. The job architecture has to change first.

---

*Federal and private postings from the Skillenai job index (2026), both under the same relevance filter; the remote-work time series uses the open [loyoladatamining/usajobs](https://huggingface.co/datasets/loyoladatamining/usajobs) USAJOBS corpus (2022–2026), which reaches further back than our index. Skill measurement is raw-text phrase matching applied identically to both sides. [Full methodology and code](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-tech-skills-wall).*
