Out of 222 AI/ML/DS skills, exactly one scores positive on all five difficulty signals.

It's not an LLM concept. It's a numerical computation library: JAX — Google's NumPy-with-a-compiler, the thing that powers Gemini, Gemma, and parts of Claude.

We measured 5 independent signals: seniority gating, salary premium, supply/demand ratio, employer concentration, and vocabulary jargon density. Most "hard" skills score high on 2 or 3. JAX scores top-decile on every one.

— +17.6% salary premium controlling for role/country/seniority
— 90% of JAX postings are senior or above
— Lowest blog-to-job ratio of any tested skill (0.27 — vs transformer at 4.42)
— Specialist-level employer concentration (Waymo, Anthropic, Apple, frontier labs)
— Second-densest technical vocabulary in our blog corpus

For contrast, prompt engineering — the AIE skill everyone is supposedly racing to acquire — carries a -21.6% salary coefficient AND the lowest jargon density tied with SQL. The labor market is signalling four ways at once that prompt engineering is a commodity.

The career implication for Data Scientists: AI Engineer is the longest paper jump on the role taxonomy (Jaccard 0.154) but the easiest in effort terms. The missing skills are LangGraph, vector databases, RAG, prompt engineering — bottom half of the difficulty distribution.

Research Scientist is the opposite. Shorter paper jump, but the missing skills are generative modeling, JAX, distributed training, RL, post-training. Top-decile across the board.

Same Jaccard distance, completely different climbs.

What's in your stack — the easy AI plumbing, or the hard AI tooling?

Full analysis (5 difficulty signals, 222 skills, 11 role transitions) in the comments.

<!-- model score
v4 (5-signal redesign — dropped academic-depth + prereq-depth, added supply/demand, employer HHI, vocabulary IDF):
- impressions: 1642  (vs 2277 v3, -28%)
- engagements: 22    (vs 30 v3, -27%)
- followers_3d: 15.4 (vs 19.4 v3)

Score dropped vs v3 because draft is longer (218 words vs ~190) and reads more analytical. Suggestion to move URL out of body fired — but only URLs in this comment block, not in the actual post body. False positive; ignore.

First-comment URL: https://github.com/skillenai/skillenai-notebooks/tree/master/skill-difficulty
Blog post (when published): https://skillenai.com/blog/the-hardest-skill-in-ai-hiring-is-jax
-->
