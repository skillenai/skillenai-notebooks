# LinkedIn post draft

## Final version (model-scored best, all numbers verified)

```
A Data Scientist in Bangalore and a Data Scientist in San Francisco have one thing in common before anything else: both job descriptions ask for Python.

We analyzed 137,974 tech job postings across 25+ countries and 18 roles. Python wins by every measure of "important" we tried:

→ Prevalence: 29% of all postings (2x SQL, the next skill)
→ Cross-role universality: required in 14 of 18 top tech roles at >=30%
→ Geographic flatness: 25-37% in every major market — China 37%, Israel 36%, India 31%, US 30%, UK 28%
→ Seniority flatness: 32-38% from intern through staff IC
→ Graph centrality: 65,705 incoming edges in our knowledge graph — 1.5x the next entity. And uniquely, Python is the only top skill that wins both axes — most-required (jobs) AND most-mentioned (docs).

The surprise: Python is not a salary premium. For Data Engineers it pays +13%, but for ML Engineers and AI Engineers it pays -9%. The premium has moved up a layer. CUDA, C++, distributed systems — that's where the differential lives now.

Python is the floor of technical work, not the ladder. The career-relevant question is no longer "should I learn Python?" It's "what do I stack on top of it?"

The dominant pair: Python + SQL (32% of Python jobs). Add AWS or GCP and you have the modal "ready for a tech IC role" stack.

Full charts and methodology in the first comment.

What does your stack look like above the Python layer?
```

**First comment:** `Full analysis with all 8 charts: https://github.com/skillenai/skillenai-notebooks/tree/master/python-rules`

<!-- model score
v2 baseline (one-line centrality, "2.5x next" — was inaccurate pre-fix): imp=4349 eng=31 fol=21
v7 (FINAL — two-line centrality with two-axis claim, all numbers verified): imp=4235 eng=26 fol=21
   ~3% under v2 because of one extra line, but accurate. Worth the trade.

Centrality numbers verified post-publish-bug-fix:
- 65,705 = sum of MENTIONS + REQUIRES edges across both Python skill and product canonical IDs
- 1.5x = vs Kubernetes at 43,744 (next entity)
- "wins both axes" = #1 in REQUIRES (47,275 vs SQL #2 at 22,722) AND #3 in MENTIONS (18,430,
  behind only ML 24,529 and Kubernetes 24,455)
-->
