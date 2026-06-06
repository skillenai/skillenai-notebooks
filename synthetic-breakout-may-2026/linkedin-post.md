The breakout AI blog author of May 2026 doesn't exist.

We pulled bylines from 423,802 tech and AI blog posts in the Skillenai index, looking for who broke out in May vs April on volume or per-post authority. The number one answer was a man named Daniel Mercer — 0 posts in April, 381 in May, average per-post authority in the top 5% of the entire index.

He's not real. He's one of 221 synthetic bylines a single content-farm operator switched on in May, attached to LLM-generated MLOps, RAG, and AI playbook content, spread across 333 cheap cloud-themed domains.

The smoking gun is structural:
• Same 333 domains in April: 8,583 posts, 99.6% with NO byline
• Same 333 domains in May: 1,856 posts, 221 distinct fake bylines
• 141 of those domains host 2+ of the personae. deployed.cloud alone hosts 8 different "authors"
• Daniel Mercer "wrote" 381 posts in 20 days across 208 distinct domains — real bloggers don't behave like this

The April content was anonymous. In May the operator added a layer of fake humans to the same pipeline. That's the breakout: an attribution-coating campaign, executed across an entire SEO network on May 12.

If you rank AI bloggers by volume or by per-post authority, you are ranking the content farms. The real human breakouts in May — Rod Trent on MSFT security, Ruben Hassid on AI, Alex Merced on Apache Iceberg, Marin Ivezic on PQC — sit underneath and look quaint by comparison.

If you're using LLM-generated blog corpora to train retrieval, evals, or ML models for the labor market, you are now training on synthetic bylines too. The next-generation tell isn't anonymity — it's structural: shared domains, shared topics, shared LLM cadence.

How are you separating real authorship from synthetic bylines in your own AI and ML feeds?

Full analysis with charts and the 333-domain denylist in the comments.

<!-- first comment to add after posting:
https://skillenai.com/blog/the-breakout-blog-author-of-may-2026-doesn-t-exist
https://github.com/skillenai/skillenai-notebooks/tree/synthetic-breakout-may-2026/synthetic-breakout-may-2026
-->

<!-- model score (linkedin_scoring v? on 2026-06-05, final after 3 iterations):
v1 baseline:   impressions=840.3   engagements=9.9   followers_3d=11.8
v2 +acronyms:  impressions=1006.4  engagements=12.5  followers_3d=12.4
v3 tightened:  impressions=1006.2  engagements=12.6  followers_3d=12.4  <- shipped

Suggestions applied: added capitalized acronyms (LLM, RAG, MLOps, PQC, MSFT, ML, SEO).
Suggestions skipped: "add an exclamation" (per skill memory: unreliable, prior application
caused -5% impressions / -13% engagements).
-->
