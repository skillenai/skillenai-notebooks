import json, pandas as pd, anthropic, concurrent.futures as cf, time
cl = anthropic.Anthropic()
CATS = {
 "define_quality": "Define what good looks like: success criteria, quality bar, eval metrics/KPIs, eval strategy",
 "error_analysis": "Review AI outputs or traces, find and categorize failure modes, manual QA of AI behavior",
 "datasets": "Build golden sets, ground truth, eval datasets, or annotation/labeling for evaluation",
 "write_evals": "Write or design evals themselves: test cases, rubrics, LLM-as-judge, automated graders",
 "infrastructure": "Build eval harnesses, pipelines, frameworks, CI/regression suites, eval instrumentation or observability",
 "run_monitor": "Run offline/online evals, A/B tests, benchmark or compare models, monitor production quality/regressions",
 "decide_ship": "Use eval results to make decisions: launch/release gates, model selection, prioritization, communicate results to stakeholders",
 "safety": "Safety, red-teaming, hallucination, bias, or compliance evaluation",
}
props = {k: {"type": "boolean", "description": v} for k, v in CATS.items()}
props["depth"] = {"type": "string", "enum": ["leads", "builds", "fluency", "not_ai_eval"],
  "description": "leads = owns/drives/establishes the eval approach; builds = hands-on doing eval work without owning it; fluency = only expected to understand/be familiar with evals or tools; not_ai_eval = the excerpt is not about evaluating AI/LLM systems (e.g. evaluating vendors, candidates, or which AI tools to adopt)"}
TOOL = {"name": "record", "description": "Record the AI-evaluation responsibilities a job posting assigns to the hire.",
        "input_schema": {"type": "object", "properties": props, "required": list(props)}}
SYS = "You label job-posting excerpts. Only mark a responsibility true if the excerpt assigns it to the hire. Evaluating AI/LLM/ML model systems counts; evaluating vendors, candidates, or technologies to adopt does not."
def run(snip):
    for i in range(6):
        try:
            r = cl.messages.create(model="claude-sonnet-5", max_tokens=300, system=SYS, tools=[TOOL],
                tool_choice={"type": "tool", "name": "record"},
                messages=[{"role": "user", "content": f"Excerpt (sentences mentioning evaluation):\n\n{snip}"}])
            return next(b.input for b in r.content if b.type == "tool_use")
        except anthropic.APIError as e:
            last = e; time.sleep(2 ** i)
    raise RuntimeError(f"exhausted: {last}")
s = pd.read_parquet("snippets.parquet"); s = s[s.snip.str.len() > 0].reset_index(drop=True)
with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(run, s.snip))
out = pd.concat([s, pd.DataFrame(res)], axis=1)
out.to_parquet("classified_sonnet.parquet"); print(len(out)); print(out.depth.value_counts())
