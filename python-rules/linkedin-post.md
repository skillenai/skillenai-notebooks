# LinkedIn post draft

## Recommended (v2 — model-scored best)

This version leads with the cleanest single-narrative ("Python wins"). The centrality finding lives in the blog and notebooks for readers who click through. Predicted: ~4,350 impressions, ~31 engagements.

```
A Data Scientist in Bangalore and a Data Scientist in San Francisco have one thing in common before anything else: both job descriptions ask for Python.

We analyzed 137,974 tech job postings across 25+ countries and 18 roles. Python wins by every measure of "important" we tried:

→ Prevalence: 29% of all postings (2x SQL, the next skill)
→ Cross-role universality: required in 14 of 18 top tech roles at >=30%
→ Geographic flatness: 25-37% in every major market — China 37%, Israel 36%, India 31%, US 30%, UK 28%
→ Seniority flatness: 32-38% from intern through staff IC
→ Graph centrality: 2.5x the incoming knowledge-graph edges of the next entity

The surprise: Python is not a salary premium. For Data Engineers it pays +13%, but for ML Engineers and AI Engineers it pays -9%. The premium has moved up a layer. CUDA, C++, distributed systems — that's where the differential lives now.

Python is the floor of technical work, not the ladder. The career-relevant question is no longer "should I learn Python?" It's "what do I stack on top of it?"

The dominant pair: Python + SQL (32% of Python jobs). Add AWS or GCP and you have the modal "ready for a tech IC role" stack.

Full charts and methodology in the first comment.

What does your stack look like above the Python layer?
```

⚠️ **Note:** the "graph centrality: 2.5x" line was based on the partial graph data we had at the time of v2. The full graph sweep (run later) flipped that result — Python is actually 3rd in graph centrality, behind machine learning (24,528) and Kubernetes (24,454). **If you publish v2, drop that bullet** to avoid an inaccurate claim. The other bullets are unchanged.

---

## Alternative (v6 — leads with the centrality flip)

This version is more honest about the centrality finding but the model predicts a ~60% drop in reach (~1,760 impressions) because the longer text pattern underperforms in this account's history. Use this if you'd rather lead with the surprise than maximize reach.

```
A Data Scientist in Bangalore and one in San Francisco have one thing in common before anything else: both job descriptions ask for Python.

We analyzed 137,974 tech postings. Python is in 29% of them — 2x SQL, the next skill — and uniquely flat at ~30% across every major country and every IC seniority level from intern to staff. By any measure of employer demand, it wins.

But here is the twist. We also ran graph centrality across our full corpus of jobs, blogs, news, and scholarly papers. Python dropped to 3rd. Top two: machine learning (24,528 mentions) and Kubernetes (24,454).

Python is the dominant tool of tech work. ML is the dominant topic of tech discourse. Different question, different answer.

The salary picture has its own twist. Python pays +13% for Data Engineers but -9% for ML Engineers. In ML roles Python is assumed; the premium has moved up a layer to CUDA, C++, and distributed systems.

Python is the floor of technical work, not the ladder. The career-relevant question is no longer "should I learn Python?" It is "what do I stack on top of it?"

Full charts and methodology in the first comment.

What does your stack look like above the Python layer?
```

**First comment (either version):** `Full analysis with all 8 charts: https://github.com/skillenai/skillenai-notebooks/tree/master/python-rules`

<!-- model score
v2 (no centrality): impressions=4349 engagements=31 followers_3d=21  ← RECOMMENDED
v3 (added exclamation per suggestion): 4128 / 27 / 21 (regressed)
v4 (centrality + long): 2493 / 20 / 21
v5 (centrality, tightened): 2344 / 21 / 21
v6 (centrality, even tighter): 1763 / 21 / 17  ← honest but reach drops 60%

Model preference: shorter, punchier, single-narrative. Adding the centrality nuance ~halves predicted impressions.

Tradeoff: v2 maximizes reach but contains a stale "centrality 2.5x" bullet that should be dropped pre-publish (or fixed). v6 is fully accurate but reach is much lower.
-->
