A new AI buzzword went viral on X this week. I searched 870,000 documents for it — and 2 out of every 3 times it appeared, it meant something completely different.

The term is "loop engineering." On June 7, one post coined it; three days later it was everywhere. So I went looking across our blog, news, and job corpus to see what a buzzword looks like at 72 hours old.

The idea itself is real: stop prompting your AI coding agent turn by turn, and instead design the loop that prompts it for you. You write the definition of "done" once; the agent runs, gets graded, revises, repeats. Its own advocates are blunt about the lineage — "loop engineering is replacing prompt engineering." Several tie it to Claude Fable 5 and long-horizon agentic autonomy.

But here's the part every trend-tracker should sit with.

Search the raw string "loop engineering" and you get 27 hits. Only 9 are the actual AI term. The other 18: hardware-in-the-loop test roles, human-in-the-loop ML supervision, recruiter boilerplate ("Loop: Engineering interview"), a protein-folding job, a growth-marketing funnel.

The newborn AI buzzword is a thin sliver riding on top of five older meanings. That ambiguity is exactly why it spreads so fast — it sounds familiar before anyone tells you what it means.

The lineage is the real signal:
- Prompt engineering: mature, ~250 mentions per 10K blog posts
- Context engineering: took off mid-2025, ~90 per 10K
- Loop engineering: basically zero, because we caught it on day three

Each term is an order of magnitude smaller than its parent — because we keep catching them earlier in the cycle.

One caveat I won't hide: X isn't in our corpus, so I can't chart the thing that started this. I'm measuring the spillover into the durable record — blogs and newsletters — not the origin.

If loop engineering follows context engineering's curve, it crosses into real volume by late 2026. Testable. We'll see.

What's the shortest-lived AI buzzword you've watched come and go?

Full analysis in the comments.

<!-- first comment: https://github.com/skillenai/skillenai-notebooks/tree/master/loop-engineering (and the published blog URL once live) -->

<!-- model score (scripts/linkedin_scoring/score.py)
v1 (June-7-hook, list lineage):     impressions 934  | engagements 12.0 | followers_3d 15.3
v2 (counterintuitive hook, +acronyms, list lineage): impressions 1096 | engagements 13.2 | followers_3d 13.8  <-- SELECTED
v3 (v2 but prose lineage):          impressions 1088 | engagements 12.1 | followers_3d 13.5  (reverted: prose hurt engagements)
Drivers: word_count/dow/followers_at_post positive; line_count, upper_word_ratio, has_link negative.
Did NOT apply the "add an exclamation" suggestion (historically unreliable, -5%/-13% when blind-applied).
Note: CV R^2 ~0.27 impressions / 0.40 engagements — treat as relative ranking, not absolute forecast.
-->
