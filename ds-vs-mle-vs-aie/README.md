# Data Scientist vs ML Engineer vs AI Engineer: Skills Comparison

**Date:** 2026-04-08
**Source:** Skillenai `/v1/analytics/skills-by-role` endpoint (entity-resolved, REQUIRES edges)

---

## Dataset Overview

| Role | Job Postings | Query Aliases |
|------|-------------|---------------|
| Data Scientist | 1,298 | Data Scientist |
| ML Engineer | 1,318 | ML Engineer, Machine Learning Engineer |
| AI Engineer | 599 | AI Engineer, Artificial Intelligence Engineer |

Total: **3,215 unique job postings** across the three roles.

---

## Full Cross-Tabulation (% of jobs requiring each skill)

Values are the percentage of job postings for that role that list the skill as required.

| Skill | DS % | MLE % | AIE % | Profile |
|-------|------|-------|-------|---------|
| Python | 72.4 | 57.2 | 61.4 | Core (all roles) |
| Machine Learning | 51.1 | 75.0 | 36.6 | MLE-leaning |
| SQL | 57.2 | 12.1 | 9.7 | DS-dominant |
| PyTorch | 12.6 | 40.7 | 18.4 | MLE-leaning |
| AWS | 12.6 | 19.0 | 22.7 | AIE-leaning |
| TensorFlow | 12.9 | 27.5 | 13.5 | MLE-leaning |
| Data Pipelines | 18.3 | 17.5 | 11.9 | Core (all roles) |
| A/B Testing | 26.0 | 9.7 | 8.2 | DS-dominant |
| LLMs | 8.6 | 11.7 | 22.2 | AIE-leaning |
| Fine-tuning | 4.2 | 14.7 | 21.2 | AIE-leaning |
| Model Evaluation | 7.1 | 17.0 | 15.4 | MLE-leaning |
| Deep Learning | 10.8 | 21.8 | 6.3 | MLE-leaning |
| Prompt Engineering | 4.4 | 5.6 | 26.0 | AIE-dominant |
| CI/CD | 6.5 | 12.1 | 17.0 | AIE-leaning |
| Model Deployment | 9.2 | 18.9 | 7.2 | MLE-leaning |
| MLOps | 7.9 | 13.5 | 10.9 | MLE-leaning |
| GCP | 7.8 | 10.2 | 13.7 | AIE-leaning |
| Monitoring | 4.9 | 12.6 | 14.2 | AIE-leaning |
| Data Science | 22.5 | 4.9 | 3.5 | DS-dominant |
| scikit-learn | 14.9 | 10.0 | 5.8 | DS-leaning |
| Observability | 2.2 | 8.3 | 19.4 | AIE-dominant |
| Docker | 5.3 | 12.1 | 12.2 | MLE/AIE shared |
| Azure | 5.9 | 9.1 | 14.5 | AIE-leaning |
| Data Analysis | 20.5 | 5.5 | 3.3 | DS-dominant |
| Kubernetes | 3.8 | 13.3 | 12.2 | MLE/AIE shared |
| Pandas | 15.9 | 6.1 | 4.5 | DS-dominant |
| Experimentation | 15.6 | 6.6 | 4.3 | DS-dominant |
| RAG | 2.9 | 6.1 | 17.4 | AIE-dominant |
| LangChain | 2.9 | 3.9 | 18.7 | AIE-dominant |
| Model Training | 3.8 | 17.5 | 3.5 | MLE-dominant |
| Feature Engineering | 10.2 | 10.1 | 4.5 | DS/MLE shared |
| Generative AI | 6.0 | 7.4 | 10.0 | Core (all roles) |
| NLP | 8.4 | 7.1 | 7.2 | Core (all roles) |
| R | 20.7 | 1.4 | 0.5 | DS-exclusive |
| Data Modeling | 15.0 | 3.0 | 4.5 | DS-dominant |
| TypeScript | 1.5 | 3.4 | 17.4 | AIE-dominant |
| Testing | 3.9 | 7.1 | 10.7 | AIE-leaning |
| Data Visualization | 19.3 | 1.7 | 0.5 | DS-exclusive |
| Computer Vision | 4.6 | 11.9 | 4.5 | MLE-dominant |
| Distributed Systems | 0.7 | 8.6 | 11.4 | AIE-leaning |
| Vector Databases | 2.0 | 3.4 | 15.0 | AIE-dominant |
| Model Monitoring | 6.5 | 10.1 | 3.5 | MLE-leaning |
| APIs | 3.9 | 5.1 | 11.0 | AIE-leaning |
| Predictive Modeling | 16.0 | 1.4 | 1.3 | DS-exclusive |
| Spark | 9.5 | 8.2 | 1.0 | DS/MLE shared |

---

## Shared Foundation

Six skills appear in >10% of job postings across all three roles. These form the baseline competency for anyone working in applied ML/AI:

| Skill | DS | MLE | AIE |
|-------|-----|------|------|
| Python | 72.4% | 57.2% | 61.4% |
| Machine Learning | 51.1% | 75.0% | 36.6% |
| PyTorch | 12.6% | 40.7% | 18.4% |
| AWS | 12.6% | 19.0% | 22.7% |
| TensorFlow | 12.9% | 27.5% | 13.5% |
| Data Pipelines | 18.3% | 17.5% | 11.9% |

Python is the universal language of all three roles. Machine Learning is the shared domain, though the depth varies (MLE at 75%, DS at 51%, AIE at 37%).

---

## Distinctive Skills by Role

Skills appearing in >15% of one role's postings but <5% in the other two:

### Data Scientist (6 distinctive skills)

| Skill | % |
|-------|---|
| Data Science | 22.5% |
| R | 20.7% |
| Data Visualization | 19.3% |
| Predictive Modeling | 16.0% |
| Causal Inference | 15.3% |
| Data Modeling | 15.0% |

The DS distinctive skill set is **statistical, analytical, and business-facing**. R, causal inference, and predictive modeling reflect a role grounded in hypothesis testing and decision science. Data visualization and data modeling indicate the expectation that DS professionals communicate findings to non-technical stakeholders.

### ML Engineer (1 distinctive skill)

| Skill | % |
|-------|---|
| Model Training | 17.5% |

MLE has the fewest truly distinctive skills because it occupies the **middle ground** between DS and AIE. Its identity is defined more by the combination and depth of shared skills (PyTorch at 41%, deep learning at 22%, model deployment at 19%) than by unique ones. The model training signal reflects the core MLE responsibility: taking models from prototype to production-grade.

### AI Engineer (3 distinctive skills)

| Skill | % |
|-------|---|
| LangChain | 18.7% |
| TypeScript | 17.4% |
| Vector Databases | 15.0% |

The AI Engineer distinctive skill set is **LLM-native and application-layer**. LangChain and vector databases signal a role built around orchestrating foundation models (not training them). TypeScript at 17.4% is the most surprising signal — it makes AIE the most full-stack of the three roles, expected to build user-facing applications, not just backend model pipelines.

---

## Role Identity Profiles

### Data Scientist: The Analyst-Scientist

**Core identity:** Statistical reasoning + business communication

The DS role is anchored in SQL (57%), experimentation (A/B testing at 26%, experimentation at 16%), and statistical methods (causal inference, predictive modeling). It is the only role where R appears meaningfully (21%). Data Scientists are expected to own the full analytical loop: formulate hypotheses, query data, build models, and visualize results.

**DS hires for:** Analytical thinking, statistical rigor, communication to stakeholders.

### ML Engineer: The Model Builder

**Core identity:** Deep ML + production infrastructure

MLE has the highest machine learning demand (75%) and the deepest framework expertise (PyTorch 41%, TensorFlow 28%). The role spans model training through deployment: feature engineering (10%), model training (18%), model deployment (19%), model monitoring (10%), MLOps (14%). Computer vision (12%) and reinforcement learning appear almost exclusively in MLE postings, reflecting the role's connection to specialized ML domains.

**MLE hires for:** Deep ML knowledge, systems engineering, model lifecycle management.

### AI Engineer: The LLM Application Builder

**Core identity:** Foundation model orchestration + full-stack delivery

AIE is defined by the LLM stack: prompt engineering (26%), LLMs (22%), fine-tuning (21%), RAG (17%), LangChain (19%), vector databases (15%). But it also has the strongest devops signals — observability (19%), CI/CD (17%), monitoring (14%), Docker (12%), distributed systems (11%). The TypeScript requirement (17%) places this role at the application layer, building products on top of models rather than training the models themselves.

**AIE hires for:** LLM fluency, product engineering, full-stack delivery.

---

## Key Insights

### 1. The Three Roles Occupy Distinct Layers

The data reveals a clean stratification:

- **DS** operates at the **data/insight layer** — SQL, stats, visualization, experimentation
- **MLE** operates at the **model/training layer** — PyTorch, deep learning, model lifecycle
- **AIE** operates at the **application/orchestration layer** — LLM APIs, RAG, vector DBs, TypeScript

### 2. AI Engineer Is the Newest and Most LLM-Native Role

With only 599 postings vs ~1,300 for DS and MLE, AIE is still emerging. But its skill profile is sharply differentiated: prompt engineering, RAG, LangChain, and vector databases are near-exclusive to this role. AIE represents the market's response to LLMs creating a new application-layer abstraction.

### 3. SQL Is the Great Divider

SQL is the single largest differentiator in the dataset: 57% for DS vs 12% for MLE vs 10% for AIE. If a job posting requires SQL fluency, it's almost certainly a DS role. This reflects the fundamental orientation of DS toward data querying and analysis rather than model building or application development.

### 4. MLE Is the Bridge Role

ML Engineer shares significant skill overlap with both DS (scikit-learn, feature engineering, Spark) and AIE (LLMs, fine-tuning, Docker, Kubernetes). Its distinctive identity comes from the combination and depth rather than unique skills. MLE is where DS and AIE converge in the model training and deployment pipeline.

### 5. Cloud Provider Preferences Vary

AIE shows the most multi-cloud distribution (AWS 23%, Azure 15%, GCP 14%), while DS is the least cloud-focused (AWS 13%, others <8%). This suggests AIE roles are more infrastructure-aware and often deployed across varied enterprise environments.

### 6. The TypeScript Signal

TypeScript appearing in 17% of AIE postings but <4% for the other two is a strong signal that AI Engineers are expected to build user-facing applications. This distinguishes AIE from MLE (backend/pipeline) and DS (analysis/notebooks) in a way that few other skills do.

---

## Methodology

- Data sourced from `GET /v1/analytics/skills-by-role` using entity-resolved role names
- ML Engineer results merge aliases: "ML Engineer" + "Machine Learning Engineer"
- AI Engineer results merge aliases: "AI Engineer" + "Artificial Intelligence Engineer"
- Percentages calculated as (skill count / total jobs for role) * 100
- "Distinctive" defined as >15% in one role and <5% in the other two
- "Shared foundation" defined as >10% in all three roles
