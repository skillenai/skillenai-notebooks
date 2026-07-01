# LinkedIn post

*Post the blog link as the FIRST COMMENT, not in the body (inline links suppress reach). Swap in the public blog URL once the post is published.*

---

AI Engineer is the only tech role still hiring 2-for-1. Data Scientist? It just went negative.

We combined Skillenai's job-postings data with Live Data Technologies' 95M+ profiles to map who actually becomes an AI Engineer — demand and supply at once.

The finding that stopped me: among 5 adjacent roles, AI Engineer is the only one where ~2 people arrive for every 1 who leaves (1.97x). ML Engineer, Data Engineer, and Software Engineer all sit near replacement (~1.1x). Data Scientist is at 1.02x — its net additions peaked in 2019 and turned negative in 2025.

But this is NOT a rename of Data Science or ML. The skill fingerprint is a genuinely different job. LLM shows up in 50% of AI Engineer postings vs 10% for Data Scientist. Agentic 39%, prompt engineering 25%, RAG 14%. Meanwhile ML Engineers own PyTorch and Data Scientists own statistics.

Where do they come from? Software Engineers are the biggest feeder. Where do they go? Back to ML and research — or up into founder and leadership roles. Same ~20% annual churn as everyone else. It just fills twice as fast.

Pay lands like a premium SWE: ~$190K midpoint, above DS, just below the ML specialist.

The takeaway for DS and SWE folks: this is the highest-momentum move on the board right now — and it's real reskilling, not a title swap.

Which role do you think stalls next?

---

**First comment:** Full analysis, charts, and methodology → [blog URL once published]  ·  Data + code: https://github.com/skillenai/skillenai-notebooks/tree/master/ai-engineer-talent-flows

<!-- model score (scripts/linkedin_scoring/score.py), final draft:
predicted impressions: 4,782  (cv_r2 0.27, mae ~1,204)
predicted engagements: 56     (cv_r2 0.40, mae ~17)
predicted followers_3d: 18
Top positive drivers: upper_word_ratio (acronyms: AI/LLM/RAG/ML/DS/SWE), ends_with_question.
Only suggestion returned was "add an exclamation" — declined: it's the known-unreliable
suggestion and exclamation_count was a NEGATIVE per-draft driver here. No inline URL (link → first comment),
no unicode bullets. Not iterated further — draft already top-tier and only suggestion was adversarial.
-->
