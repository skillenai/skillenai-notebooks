The hardest skill in AI hiring isn't an LLM concept. It's a numerical computation library.

We scored 222 AI/ML/DS skills on four independent difficulty signals — how senior the postings asking for it are, how much salary premium it commands controlling for role and location, how academically deep it is, and how many other skills it presupposes.

The skill that combines all of them in the way employers actually pay for is JAX — Google's NumPy-with-a-compiler library that powers Gemini, Gemma, and parts of Claude.

— +17.3% salary premium controlling for role/country/seniority (3rd-highest in 124-skill regression)
— 90% of JAX postings are senior or above
— Almost no scholarly footprint (it's a tool, not a research topic — papers cite the methods, not the framework)
— Deeper prerequisite stack than most tooling skills

For contrast, prompt engineering — the AIE skill everyone is supposedly racing to acquire — carries a -21.1% salary coefficient. Second-lowest in the entire panel.

The career implication for Data Scientists: AI Engineer is the longest paper jump on the role taxonomy (Jaccard 0.154) but the easiest in effort terms. The missing skills are LangGraph, vector databases, RAG, prompt engineering — all bottom-half of the difficulty distribution.

Research Scientist is the opposite. Shorter paper jump, but the missing skills are diffusion models, JAX, distributed training, RL, post-training. Top-decile difficulty across the board.

Same Jaccard distance, completely different climbs.

What's in your stack — the easy AI plumbing, or the hard AI tooling?

Full analysis (4 difficulty signals, 222 skills, all 11 role transitions) in the comments.

<!-- model score
v2 (URL moved to first comment per scorer suggestion):
- impressions: 2280  (vs 2319 v1, -1.7%)
- engagements: 30  (vs 30 v1, same)
- followers_3d: 19.3  (vs 17.3 v1, +12%)

Top positive drivers: dow, followers_at_post, upper_word_ratio, word_count, char_count, "scientist" n-gram (0.56)
Top negative drivers: has_link, hour, line_count, exclamation_count
Suggestion to add exclamation skipped per skill SKILL.md note (verified unreliable).

First-comment URL: https://github.com/skillenai/skillenai-notebooks/tree/master/skill-difficulty
Blog post (when published): https://skillenai.com/blog/the-hardest-skill-in-ai-hiring-is-jax
-->
