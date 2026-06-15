I deleted the agent framework behind our AI chat! No LangGraph. No FastAPI orchestration. No MCP in the loop.

It runs on four primitives now: a file system, a bash shell, a code sandbox, and our own API. It is far more capable than the version I would have shipped in 2025.

The 2025 stack made one mistake. It answered three different questions with one architecture. There are actually three surfaces, each with its own right answer:

- Reaching users inside someone else's chat (ChatGPT, Gemini)? Build an MCP server. That is an integration play, and it is still the right call.
- Reaching Claude Code users? Ship an API plus skills, and let coding agents drive your product directly.
- Building your own chat? Give the agent a computer: file, bash, sandbox, your API. Delete the orchestration graph.

I assumed this was just my taste. So I checked Skillenai data across 220K job postings, 445K blog posts, and 141K news articles.

In tech news, the leading indicator, low-level agent runtimes went from about 30% to 71% of framework-vs-runtime mentions across 2026. Orchestration-framework mentions roughly halved. MCP held steady. It is the integration layer, not the casualty.

The catch: hiring is two surfaces behind. Job postings still ask for the 2025 framework stack over low-level runtime skills by about 12 to 1.

The frontier has moved. The job market has not priced it in yet. That gap is the opportunity.

For a chat app you own, would you still reach for an orchestration framework in 2026, or hand the model a terminal?

<!--
FIRST COMMENT (post the blog link here, not in the body — keeps reach high):
Full analysis, charts, and method: <blog permalink once published>

model score (scripts/linkedin_scoring/score.py), final draft:
  impressions ~1037  | engagements ~12.1 | followers_3d ~16.2
  cv_r2: impr 0.27, eng 0.40 (absolute predictions noisy; use for relative ranking)
  Levers hit: ends_with_question (+), acronym-heavy upper_word_ratio (MCP/API/AI/LangGraph), ~290 words, no link in body.
  Iteration: v1 baseline 1036.6/11.7; v2 (+exclamation in hook) 1037.4/12.1 kept (slight eng gain, no impr penalty);
  v3 (punchier hook + longer closing Q) 990.8/11.7 rejected (-4.5% impressions). Stopped at v2 (<2% impr gain).
-->
