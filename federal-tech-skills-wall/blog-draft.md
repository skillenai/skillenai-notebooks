# BLOG DRAFT (ready to post — pending author's go-ahead)

**Title:** The Federal Government Posted One ML Engineer Job in Six Months

**Category:** insights-and-analytics · **Tags:** federal jobs, data science, machine learning engineer, public sector, AI engineer, tech careers · **Author:** Skillenai AI Analyst · **Cover:** 01_missing_roles.png

**Excerpt:** The federal-private tech divide isn't only the pension. Under identical titles, the two sectors ask for different tools — and the modern data/ML/AI-engineering roles that define private tech barely exist as federal jobs.

---

Two weeks ago we [priced the federal tech bargain](https://skillenai.com/blog): lower pay and almost no mobility, in exchange for near-total job security — with a back-loaded **pension** at the center holding the trade together. That explained why federal tech workers so rarely *leave*.

It left a thread hanging. Even the youngest, un-vested federal workers quit at only ~5% — far below their private peers — which we chalked up to "non-transferable experience binding from day one, before any pension handcuff exists." Data scientist Abigail Haddad put it more sharply: *"lack of movement is about skill set / tech stack as much as it's about pension… you'd see more movement if you looked at folks who were more hands-on-keyboard coders."*

She's right. There's a **second wall**, independent of the pension: the *work itself* is different. Under identical job titles, federal and private tech postings ask for different tools — and the role categories that define private tech mostly **don't exist** as federal jobs at all.

## The federal government posted one ML Engineer job in six months

![Federal vs private counts for modern data roles](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/bOo8Yjvzq-Y-01-missing-roles.png)

Start with the simplest question: how many of each data role does federal hiring actually post? Across **84,016 federal postings** over six months (all occupations):

| Title | Federal (6 mo) | Private (Skillenai index) |
|---|---:|---:|
| Data Scientist | 99 | 2,181 |
| Data Analyst | 22 | 1,038 |
| **Data Engineer** | **6** | 1,758 |
| **Machine Learning Engineer** | **1** | 2,555 |
| **AI Engineer** | **2** | 848 |

Data Engineer, ML Engineer, AI Engineer, MLOps — the backbone of a modern private data organization — are functionally **not federal jobs**. The federal Data/ML/AI workforce is instead **Operations Research Analysts, Statisticians, and Data Scientists** (90% of the family): the analyst-and-researcher lineage of data work, not the engineering one.

## Same title, different job: the federal Data Scientist

Take the one title that exists on both sides and read what the postings ask for. (Federal N=107, private N=2,000; every gap is statistically significant.)

![Federal DS vs private DS skill prevalence](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/tH0ECU4VRl0-02-ds-stack-divergence.png)

The split is clean. Federal Data Scientist postings over-index on **statistics-and-reporting** — statistics (90% vs 54%), data visualization (53% vs 23%), dashboards (37% vs 27%). Private postings over-index on **code-experiment-deploy** — Python (63% vs 30%), experimentation / A-B / causal inference (34% vs **6%**), MLOps / deployment (40% vs 20%), cloud (16% vs 5%), LLM/GenAI (16% vs 3%).

The tell is the middle: **both sectors say "machine learning" at the same rate (~44%).** Federal data scientists name ML as often as anyone — they just lack the hands-on toolchain to operationalize it. It stays a *concept*, not a *deployed system*. Even federal "Data Scientist (AI)" roles turn out to be about **AI standards and evaluation policy**, not building models — verbatim: *"promotes the adoption of standards, guides, best practices, and policy for measuring and evaluating AI technology."*

> **A federal Data Scientist and a private Data Scientist share a title and a vocabulary, but not a job: one describes machine learning, the other ships it.**

## The pattern repeats: Software and Security

![Software Engineer and Cybersecurity skill divergence](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/ZaLFUBD0yIk-04-swe-security-stacks.png)

**Software Engineer** (federal N=208). Federal software runs a **legacy stack** — **COBOL appears in 9% of federal software postings and ~0% of private** — under an RMF/NIST/FISMA compliance overlay. Private software is cloud-native: AWS 25% vs 4%, Kubernetes 17% vs 3%, TypeScript 19% vs 4%.

**Cybersecurity** (federal N=778) — the sharpest divergence in the data. Federal security is clearance-and-governance: security clearance in **77%** of postings, RMF 16%; but **Python appears in 2% vs 41% private**, threat modeling 0% vs 24%, SIEM 1% vs 20%. A private "Security Engineer" is a cloud DevSecOps builder; a federal "Cybersecurity Specialist" is a cleared compliance professional.

## Why matched titles cover so little: the composition inverts

![Role families and the 2210 monolith](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/3gelzPEc6bg-03-role-composition.png)

The matched-title comparisons span only a sliver of federal hiring, because the *mix* of roles inverts:

| Role family | Federal tech | Private tech |
|---|---:|---:|
| Software/Dev (hands-on) | **6.4%** | **43.2%** |
| Data/ML/AI | 8.9% | 18.4% |
| Security/Cyber | **25.3%** | 3.1% |
| IT/Ops/Infra | 42.3% | 12.3% |
| Program/Product/Mgmt | 17.2% | 23.1% |

Hands-on software development is **~7× rarer** in federal tech; security is **~8× more common**. One occupational series — **2210 (IT Management) — is 83% of federal tech postings**, while **Data Science (1560) is 3.4%**. The hands-on-keyboard coders most able to arbitrage a pay gap by moving are exactly the population federal tech barely employs. Low mobility isn't only a handcuff on the people who are there — it's partly a question of *who's there to begin with*.

## Two more walls: clearance and the closed remote door

![Clearance wall and remote door](https://skillenai-blog-assets-prod.s3.us-east-1.amazonaws.com/uploads/2026/07/06/e955cb79-d6bf-4b65-9c50-5facd727e73f/eC8S_x0rmQo-05-other-walls.png)

**Clearance.** **70% of federal tech postings require a real security clearance** (Secret / Top Secret / SCI) — 85% in security roles — versus low single digits private. A private engineer without one can't take most federal tech jobs regardless of skill.

**Remote.** **Fully-remote federal tech is 0.3%** of postings — effectively closed — versus ~31% private. (63% are "telework-eligible," but that's situational telework tied to a duty station, not location freedom.)

## What it means

**If you're a federal tech worker thinking of leaving:** the pension is the handcuff you can feel; the skills gap is the one you can't. Operations Research, statistics-and-reporting data science, COBOL maintenance, clearance-gated compliance — the private market runs on Python, cloud, experimentation, and DevSecOps. The move is a *retraining* project, not just a resignation, which is why so few make it, vested or not.

**If you're a private engineer eyeing government:** most roles you'd recognize barely exist as federal jobs, and most that do want a clearance you can't get on your own.

**For the government:** the pipeline problem is deeper than pay. Even a fully-funded, competitively-paid hiring push would be hiring into role *categories* — analyst data science, legacy-stack software, compliance security — that don't match where technical talent is trained. Closing the pay gap wouldn't make a modern ML-engineering workforce appear. The job architecture has to change first.

---

*Federal postings from the open [loyoladatamining/usajobs](https://huggingface.co/datasets/loyoladatamining/usajobs) corpus (USAJOBS, 2025-10 → 2026-03), 2,859 tech postings with full announcement text; private postings from the Skillenai job index (2026-Q2). Skill measurement is raw-text phrase matching applied identically to both sides — the federal text matched is longer, so every "less modern tooling" result is conservative. [Full methodology and code](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-tech-skills-wall).*
