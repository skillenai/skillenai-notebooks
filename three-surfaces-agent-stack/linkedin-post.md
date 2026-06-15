Skillenai's new AI chat has no agent framework. No LangGraph. No FastAPI orchestration. No MCP in the loop.

I built it on Claude Managed Agents, on four primitives: a file system, a bash shell, a code sandbox, and our own API. It is far more capable than the version I would have shipped in 2025.

The 2025 stack made one mistake. It answered three different questions with one architecture. There are actually three surfaces, each with its own right answer:

- Reaching users inside someone else's chat (ChatGPT, Gemini)? Build an MCP server. That is an integration play, and it is still the right call.
- Reaching Claude Code users? Ship an API plus skills, and let coding agents drive your product directly.
- Building your own chat? Give the agent a computer: file, bash, sandbox, your API. Skip the orchestration graph.

I assumed this was just my taste. So I checked Skillenai data across 220K job postings, 445K blog posts, and 141K news articles.

In tech news, the leading indicator, low-level agent runtimes went from about 30% to 71% of framework-vs-runtime mentions across 2026. Orchestration-framework mentions roughly halved. MCP held steady. It is the integration layer, not the casualty.

The catch: hiring is two surfaces behind. Job postings still ask for the 2025 framework stack over low-level runtime skills by about 12 to 1.

The frontier has moved. The job market has not priced it in yet. That gap is the opportunity.

For a chat app you own, would you still reach for an orchestration framework in 2026, or hand the model a terminal?

<!--
FIRST COMMENT (post the blog link here, not in the body — keeps reach high):
Full analysis, charts, and method: <blog permalink once published>

model score (scripts/linkedin_scoring/score.py), final draft (variant B):
  impressions ~1044 | engagements ~11.5 | followers_3d ~16.1
  cv_r2: impr 0.27, eng 0.40 (absolute predictions noisy; use for relative ranking)
  Levers: declarative no-framework hook (truthful — this is the first build, never had a framework version),
  acronym-heavy upper_word_ratio (MCP/API/AI/LangGraph), ~285 words, ends with a question, no link in body.
  Hook iteration (all truthful): "without an agent framework!" 926 impr; "built on Managed Agents — skipped... entirely!" 941;
  "has no agent framework." (declarative) 1044 -> chosen. Avoided the earlier "I deleted the agent framework" hook (factually wrong).
-->
