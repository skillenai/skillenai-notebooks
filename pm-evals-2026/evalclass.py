"""Shared classifier: is a skill-entity canonical name an AI-eval skill?

STRICT     = explicitly about evaluating AI/LLM systems (AI-qualified eval, eval jargon,
             LLM-as-judge, dedicated eval tools). Counted unconditionally.
CONTEXTUAL = generic evaluation-methodology names (model evaluation, evaluation frameworks,
             error analysis, golden datasets, rubrics...). Only AI eval when the same
             posting/position also carries a GenAI skill; counted in the BROAD measure only.
Everything else (vendor/program/performance/heuristic/T&E/risk evaluation, benchmarking,
red teaming, CIS benchmarks) is excluded.
"""
import re
TOOLS = r"langsmith|langfuse|ragas|braintrust|deepeval|promptfoo|trulens|helicone|opik|patronus|humanloop|arize|galileo ai|confident ai|giskard"
AIQ = r"llms?|large language models?|language models?|genai|gen ai|generative( ai)?|ai|a\.i\.|agents?|agentic|prompts?|rag|chatbots?|conversational ai|model[- ]graded|foundation models?"
EVW = r"evals?|evaluations?|evaluating|benchmarks?|benchmarking|testing|quality"
STRICT = re.compile(
    rf"\b({TOOLS})\b"
    rf"|\b(llm|model|ai)s?[- ]as[- ](an?[- ])?judges?\b|\bllm[- ]judges?\b|\bjudge (llm|model)s?\b"
    rf"|\b({AIQ})\b.*\b({EVW})\b"
    rf"|\b(evaluation|evals?) (of|for) ({AIQ})\b"
    rf"|\bevals?\b", re.I)
EXCL = re.compile(r"vendor|supplier|program|employee|personnel|staff|risk|heuristic|usability|sensory|economic|impact|project|proposal|site |course|academic|test (and|&) evaluation|testing and evaluation|t&e|st&e|security|technical evaluation|technology evaluation|market|competitive|\bcis\b|monitoring and evaluation|stig|credit|clinical|patient|propert|financial|candidate|talent|survey|red.?team|(?<!model )performance evaluations?|(?<!model )performance evals?|employee|student|teacher|grading|evaluate-", re.I)
CONTEXT = re.compile(r"^model evaluations?$|model performance evaluation|ml model evaluation|^evaluations?$|evaluation (frameworks?|pipelines?|harness(es)?|systems?|infrastructure|tooling|tools|datasets?|metrics|methodolog(y|ies)|methods|design|suites?|loops?|workflows?|platform|strategies|techniques|rubrics?|criteria|protocols?|sets?)|(offline|online|human|automated|continuous|robust|quality|output) evaluations?|error analysis|golden (data)?sets?|golden datasets?|benchmark design|^rubrics?$|evaluation-driven|retrieval evaluation|hallucination (detection|evaluation|rate)|machine learning model evaluation|evaluation benchmarks|human-in-the-loop evaluation|safety evaluations?|accuracy evaluation|model performance evaluation", re.I)
AI_TOOL = re.compile(rf"\b({TOOLS})\b", re.I)

def classify(name: str) -> str:
    n = name.strip() if isinstance(name, str) else ""
    if not n or EXCL.search(n):
        return "none"
    if STRICT.search(n):
        # 'AI testing' / 'quality' generic words: require eval-ish or AI qualifier + eval word
        if re.fullmatch(r"(ai|a\.i\.)\s*(quality|testing)", n, re.I):
            return "context"
        return "strict"
    if CONTEXT.search(n):
        return "context"
    return "none"

GENAI = re.compile(r"\b(llms?|large language models?|generative ai|genai|gen ai|prompt engineering|retrieval[- ]augmented generation|\brag\b|ai agents?|agentic|fine[- ]tuning|embeddings?|vector (databases?|stores?|search)|langchain|langgraph|llamaindex|openai|gpt|claude|anthropic)\b", re.I)
def is_genai(name: str) -> bool:
    return isinstance(name, str) and bool(GENAI.search(name))
