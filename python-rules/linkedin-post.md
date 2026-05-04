# LinkedIn post draft

## Final version (v2 — model-scored best)

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

**First comment:** `Full analysis with all 7 charts: https://github.com/skillenai/skillenai-notebooks/tree/master/python-rules`

<!-- model score
v1 (URL in body): impressions=4289 engagements=26 followers_3d=19
v2 (URL moved to comment): impressions=4349 engagements=31 followers_3d=21  ← FINAL
v3 (added exclamation per suggestion): impressions=4128 engagements=27 followers_3d=21 (regressed; suggestion didn't help)

Top positive drivers (v2):
- upper_word_ratio (Python, SQL, AWS, GCP, IC, US, UK, etc. all caps boost)
- ends_with_question (closing CTA)
- followers_at_post (3,609)

Top negative drivers (v2):
- has_link → resolved by moving URL to first comment
- exclamation_count → kept at 0
- line_count slight penalty

n-gram positive: "scientist" (strong), "data" (small)
-->
