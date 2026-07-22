For every AI Engineer a US company hires to build with LLMs, it's asking about 2.5 generalist software engineers to do the exact same thing.

We pulled every US job posting that requires a real GenAI skill (LLMs, RAG, prompt engineering, agents, fine-tuning) and split them by role.

Dedicated AI Engineer titles: 1,048 postings. Generalist Software Engineer titles: 2,572. AI Engineer reqs are far more likely to be AI work, but the SWE base is 16x larger, so generalists win on raw volume 2.5 to 1.

Then it gets interesting, because the two groups build in completely different stacks.

Generalist SWEs asked to build AI reach for the web stack: 34% want TypeScript, 30% React, and Ruby shows up 8.7x more than it does for AI Engineers. Under half even mention Python. And 92% name no LLM orchestration framework at all: no LangChain, no LangGraph, nothing.

AI Engineers stay Python-first and name LangChain and LangGraph roughly 3x more often.

The open-source LLM ecosystem lives in Python. So a company asking for Ruby plus LLMs is, almost by definition, building something bespoke and off the beaten path.

Two teams, one mandate to build AI, very different ideas about how to do it.

Have you seen this split inside your own company?

<!-- First comment: Full analysis + charts: https://github.com/skillenai/skillenai-notebooks/tree/master/who-builds-with-llms -->

<!-- model score (scripts/linkedin_scoring/score.py, 2026-07-22)
predicted impressions 1816, engagements 20.8, followers_3d 16
top positive drivers: upper_word_ratio (acronyms), ends_with_question, url NOT in body
exclamation suggestion tested and rejected (impressions 1816 -> 1796). Kept as-is.
-->
