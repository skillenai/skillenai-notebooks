# LinkedIn draft

**Research question**: Will xAI and Cursor each die within 12 months without the SpaceX $60B call-option deal announced this week?

That's the hypothesis I set out to stress-test: Grok is bad at coding and lacks enterprise adoption; Cursor has both, but is getting squeezed by Anthropic's vertically-integrated Claude Code stack. Together they might compete with Anthropic. Alone, neither survives.

I ran it against 125K enriched job postings in the Skillenai knowledge graph. Two findings stand out.

**1. Grok is effectively absent from software-engineering hiring.**

Over the last six weeks, Cursor appeared in 1,231 job postings. Grok appeared in 73 — and 52 of those 73 are xAI's own voice-annotation contracts. Even Windsurf, the small Codeium product Cognition just acquired, nearly doubles Grok. The "bad at coding, no enterprise adoption" claim is supported with force.

[attach image: 02_jobs_ranking.png]

**2. Cursor and Claude Code are complements, not substitutes.**

561 job postings require BOTH Cursor and Claude Code. Eight require both Cursor and Grok. Real engineering teams at Sezzle, Adobe, Oracle, Grafana Labs, Ramp, and BillionToOne treat Cursor + Claude Code as a joint toolkit. If a post-acquisition pivot forces xAI-only models into Cursor, those 561 workflows break. That — not compute — is the real execution risk in the $60B deal.

The "both die in 12 months" framing is more dramatic than the numbers justify. But the data does say the deal is welding Cursor into the Musk stack and out of the Anthropic stack it's currently paired with in production engineering work.

Full breakdown with 8 charts + knowledge-graph queries: https://github.com/chiefastro/skillenai-notebooks/tree/master/xai-cursor-60b-deal
