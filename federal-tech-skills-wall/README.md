# Same Job Title, Different Job: Inside Federal vs Private Tech Hiring

*Skillenai analysis · July 2026 · federal and private postings from the Skillenai job index; the historical remote-work trend uses the open [loyoladatamining/usajobs](https://huggingface.co/datasets/loyoladatamining/usajobs) USAJOBS corpus (2022–2026), which reaches back further than our index.*

Two weeks ago we [priced the federal tech bargain](https://github.com/skillenai/skillenai-notebooks/tree/master/federal-tech-broken-bargain): lower pay and almost no mobility, in exchange for near-total job security, with a back-loaded **pension** holding the trade together. That explained why federal tech workers so rarely *leave*.

It left one thread hanging. Even the youngest, un-vested federal workers quit at only ~5% — far below their private peers — which we attributed to "selection and **non-transferable experience** binding from day one, before any pension handcuff exists." Data scientist [Abigail Haddad](https://www.linkedin.com/in/abigail-haddad/) put it more sharply: *"lack of movement is about skill set / tech stack as much as it's about pension… you'd see more movement if you looked at folks who were more hands-on-keyboard coders."*

She's right, and this post shows what that non-transferable experience actually *is*. There's a **second wall**, independent of the pension: under identical job titles, federal and private tech postings ask for different tools; and several of the role categories that define private tech barely exist as federal jobs at all.

**TL;DR** (federal and private both from the Skillenai job index, 2026; ~1,345 federal tech postings)
- **Same title, different job.** A federal Data Scientist posting is *statistics-and-reporting* (statistics 96%, data-viz 44%); a private one is *code-experiment-deploy* (Python 63%, experimentation 34%, MLOps 40%). Both name "machine learning" equally (~40%) — only one sector tools for it.
- **Some categories barely exist federally.** In our federal tech index we count **3 Machine Learning Engineer, 5 AI Engineer, 17 Data Engineer, and 0 MLOps** postings — versus thousands of each in the private index. The federal data workforce is Data Scientists, **Operations Research Analysts, and Statisticians**.
- **Cybersecurity is the sharpest split.** Federal security is clearance-and-governance (security clearance **92%**, RMF 11%); private security is hands-on (Python **41%** vs 2%, threat modeling 24% vs 0%, cloud/IaC 28–39% vs 1–3%).
- **Role composition inverts.** Hands-on Software/Dev is **4%** of federal tech vs **43%** private; Security is **38%** federal vs 3% private. One OPM series — 2210 (IT Management) — is **81%** of federal tech hiring.
- **Two more walls:** **58% of federal tech postings require a real security clearance** (75% in security) vs low single digits private; and — from the longer Loyola/USAJOBS history — **federal remote hiring collapsed from ~8% to 0.3%** after the January 2025 return-to-office mandate.

This is not a correction to the pension story; it's the other half of it. Low mobility is **over-determined**: even with the pension set aside, the skills don't travel.

---

## Data & method

- **Federal & private:** the Skillenai job index (`prod-enriched-jobs`), US postings, 2026, spam employer (Speechify) excluded. Federal = `sector=public` (USAJOBS, ~1,345 tech postings after our standard R&D-relevance filter); private = everything else, ~2,000 postings sampled per matched role. **Both sides run through the same ingestion and the same relevance filter**, so the comparison is single-source and apples-to-apples.
- **Skill measurement:** raw-text phrase matching applied identically to both sides on the posting body (federal median ~5.4K chars, 19 skill entities/posting; private ~5K). Structured facts (clearance, OPM series) are parsed from the same text.
- **Role mapping:** Data Scientist ↔ series 1560 + "Data Scientist"-titled; Software Engineer ↔ series 2210/1550 with a software/developer/application title; Security ↔ cyber/security/InfoSec titles.
- **The one exception — remote:** our index only reaches back to ~2026, and its historical-backfill path does not yet capture USAJOBS telework/remote fields reliably. The **remote-work time series therefore uses the Loyola/USAJOBS corpus** (2022–2026), which has the multi-year depth and a clean structured "Remote job" field. Everything else is Skillenai.

---

## Part 1 — The roles that barely exist

![Federal vs private counts for modern data roles](01_missing_roles.png)

How many of each data role does federal hiring actually post? In our federal tech index (~1,345 postings) versus the private index:

| Title | Federal | Private |
|---|---:|---:|
| Data Scientist | 129 | 2,181 |
| Data Analyst | 2 | 1,038 |
| **Data Engineer** | **17** | 1,758 |
| **Machine Learning Engineer** | **3** | 2,555 |
| **AI Engineer** | **5** | 848 |
| MLOps (any title) | **0** | — |

Data Engineer, ML Engineer, AI Engineer, MLOps — the backbone of a modern private data organization — are, functionally, **not federal jobs**. And our federal index is *already filtered for R&D/tech relevance*, which would tend to *keep* such roles if they existed — so single-digit counts are a strong signal, not a filtering artifact. The federal data workforce is instead the **analyst-and-researcher lineage**: Data Scientists, Operations Research Analysts, and Statisticians.

---

## Part 2 — Same title, different job: the federal Data Scientist

Take the one title that exists on both sides and read what the postings ask for. (Federal N=143, private N=2,000; every gap below is significant at a Bonferroni-corrected threshold.)

![Federal DS vs private DS skill prevalence](02_ds_stack_divergence.png)

The split is clean. Federal Data Scientist postings over-index on the **statistics-and-reporting** half — statistics (96% vs 54%), data visualization (44% vs 23%), dashboards/reporting (41% vs 27%), SAS/SPSS (13% vs 3%). Private postings over-index on the **code-experiment-deploy** half — Python (63% vs 43%), experimentation / A-B / causal inference (34% vs **6%**), MLOps / deployment / pipelines (40% vs 29%), cloud (16% vs 6%), LLM/GenAI (16% vs 5%).

The tell is the middle row: **both sectors say "machine learning" at nearly the same rate (~40%).** Federal data scientists aren't unaware of ML — they name it as often as anyone. What they lack is the *hands-on toolchain to operationalize it*. It stays a concept (statistics, a method, a research output) rather than a deployed system (Python, an experiment, a pipeline).

It goes further. Read a federal **"Data Scientist (AI)"** posting and the AI work turns out to be *governance*, not building — verbatim: *"Conducts research and development of metrics, measurements, and evaluation methods for… AI… promotes the adoption of standards, guides, best practices, and policy for measuring and evaluating AI technology."*

> **A federal Data Scientist and a private Data Scientist share a title and a vocabulary, but not a job: one describes machine learning, the other ships it.**

---

## Part 3 — The pattern repeats: Software and Security

![Software Engineer and Cybersecurity skill divergence](04_swe_security_stacks.png)

**Software Engineer** (federal N=98, private N=2,000) — the milder of the two. Federal software engineers use Python about as often as private ones (29% vs 31%), but they're markedly **less cloud-native** — AWS 13% vs 24%, Kubernetes/Docker 10% vs 21%, TypeScript 5% vs 19% — and carry a **security-compliance overlay** private software lacks (RMF/NIST/FISMA 7% vs 1%). Federal software modernizes *defensively* (compliance) more than *architecturally* (cloud).

**Cybersecurity** (federal N=814, private N=2,000) — the sharpest divergence in the dataset. Federal security is **clearance-and-governance**: security clearance in **92%** of postings, RMF 11%. But the hands-on toolset is nearly absent — **Python 2% vs 41%**, threat modeling **0% vs 24%**, Kubernetes/Terraform 1% vs 28%, SIEM 2% vs 20%, AWS/GCP 3% vs 39%. A private "Security Engineer" is a cloud DevSecOps builder; a federal "Cybersecurity Specialist" is a cleared compliance-and-authorization professional. Same title, opposite work.

---

## Part 4 — Why matched titles cover so little: the composition inverts

![Role families and the 2210 monolith](03_role_composition.png)

Collapse both sides into role families and the shares **invert**:

| Role family | Federal tech | Private tech |
|---|---:|---:|
| Software/Dev (hands-on) | **4.4%** | **43.2%** |
| Data/ML/AI | 13.5% | 18.4% |
| Security/Cyber | **37.8%** | 3.1% |
| IT/Ops/Infra | 31.0% | 12.3% |
| Program/Product/Mgmt | 13.3% | 23.1% |

Hands-on software development is **~10× rarer** in federal tech; security is **~12× more common**. And the whole thing is dominated by a single occupational series: **series 2210 (IT Management) is 81% of federal tech postings** (series 1560, Data Science, is ~9%). The population Abigail flagged — hands-on-keyboard coders, the workers most able to arbitrage a pay gap by moving — is exactly the population federal tech barely employs. Low mobility isn't only a handcuff on the people who are there; it's partly a **denominator problem** about who's there to begin with.

---

## Part 5 — Two more walls: clearance and the closed remote door

![Clearance wall and remote collapse](05_other_walls.png)

**Clearance.** **58% of federal tech postings require a real security clearance** (Secret / Top Secret / SCI) — 75% in security roles, 55% in IT/ops — versus low single digits in private postings. A clearance takes months to years to adjudicate and is employer-sponsored; a private engineer without one cannot take most federal tech jobs regardless of skill.

**Remote — a door that just slammed shut.** *(This is the one panel drawn from the longer Loyola/USAJOBS history, because our own index doesn't yet reach before 2026.)* The USAJOBS announcement carries an official "Remote job" designation (work-from-anywhere, no duty station). Federal tech remote hiring held at **~6–10% from 2022 through January 2025** — then **collapsed to ~0.3%**, with the drop landing precisely in Q1–Q2 2025: 7.5% (Jan) → 1.3% (Mar) → ~0% after. That timing is the federal **return-to-office executive order** (January 2025). Private tech, by contrast, still designates ~31% of tech postings fully-remote. The field is demonstrably real, not a scraping artifact: it registered a healthy 6–10% for three years before collapsing exactly when policy changed.

---

## What it means

**If you're a federal tech worker thinking about leaving:** the pension is the handcuff you can feel, but the skills gap is the one you can't. If your background is Operations Research, statistics-and-reporting data science, or clearance-gated compliance security, the private market you'd be entering runs on Python, cloud, experimentation, and DevSecOps. The move is a *retraining* project, not just a *resignation* — which is exactly why so few make it, vested or not.

**If you're a private engineer eyeing government:** several roles you'd recognize (ML Engineer, Data Engineer, cloud-native security) barely exist as federal jobs, and most that do want a clearance you don't have and can't get on your own. The door is narrower than the pay tables suggest.

**For the government:** the pipeline problem is deeper than pay. Even a fully-funded, competitively-paid federal hiring push would be hiring into role *categories* — analyst/statistician data science, compliance security — that don't match where technical talent is trained or where the frontier work happens. Closing the pay gap wouldn't, by itself, make a modern ML-engineering workforce appear. The job architecture has to change first.

---

## Reproduce it & caveats

The scripts here (`fetch_federal.py` → `federal_now.json`, `compare.py`, `make_figures.py`) reproduce every number and figure; the remote trend uses `build_federal.py` over the public `loyoladatamining/usajobs` corpus and is cached in `remote_trend.json`.

- **Single-source cross-section.** Federal and private both come from the Skillenai index under the same filter, so skill/role/clearance comparisons are apples-to-apples. The one exception is the remote trend (Loyola/USAJOBS), used only because our index lacks pre-2026 history.
- **Skill = raw-text phrase presence,** applied identically to both sides.
- **Our federal index is R&D-relevance-filtered** (same filter as private), so its role-family *shares* describe R&D-relevant federal tech, not all federal hiring; the direction of every inversion is robust, the exact percentages are filter-conditional.
- **Private index misses Big-Tech proprietary ATS** (Google/Apple/Microsoft/NVIDIA), which run their own portals.
- **The COBOL/legacy-mainframe angle from earlier drafts did not survive the switch to our own data** (0% of our federal software postings) — so this version doesn't claim it. The robust software finding is the cloud-native gap plus the compliance overlay.
- **We can't see contracting vs civil service.** Much federal↔private technical movement runs through the *contractor* channel, which neither postings dataset observes.
- **Seniority is unreliable for federal** (GS grades don't map to an IC ladder), so we don't feature it; we cite GS grade (median GS-12) instead.
