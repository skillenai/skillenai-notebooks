import re
def family(role):
    r = role if isinstance(role, str) else ""
    if re.search(r"product manag|product owner|\bapm\b|product lead", r, re.I) and not re.search(r"marketing", r, re.I): return "Product Manager"
    if re.search(r"\b(ai|genai|generative ai|artificial intelligence|llm)\b.*engineer", r, re.I) and not re.search(r"machine learning|\bml\b(?!/)", r, re.I) or re.search(r"ai/ml engineer", r, re.I): return "AI Engineer"
    if re.search(r"(machine learning|\bml\b) engineer", r, re.I): return "ML Engineer"
    if re.search(r"data scientist", r, re.I): return "Data Scientist"
    if re.search(r"software (engineer|developer)|(back[- ]?end|front[- ]?end|full[- ]?stack) (engineer|developer)", r, re.I): return "Software Engineer"
    return None
