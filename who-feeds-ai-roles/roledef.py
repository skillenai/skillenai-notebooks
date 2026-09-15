"""Single shared definition of the four AI role families, used by BOTH the
resolved-graph half and the raw-profile half so the concept cannot drift.

INCLUSION RULE (recorded per Phase 4.4 rule #4):
  IN  = seniority variants (Senior/Staff/Lead/Principal/Junior/Associate/Intern)
        + pure synonyms / spelling+abbreviation variants of the same concept.
  OUT = distinct specialisations (Computer Vision, NLP, Prompt Engineer),
        advisory titles (AI Consultant, AI Specialist), and adjacent-but-separate
        roles (Applied Scientist, Data Engineer, Data Analyst, Research Scientist).
        These stay ELIGIBLE AS FEEDERS - excluding them from the family is what
        lets them show up as genuine cross-role inflow.
"""
FAMILIES = {
"Data Scientist": {
 "33dad3c1f46beae3":"Data Scientist","b9334d03b98b5059":"Staff Data Scientist",
 "f0d3e137de198384":"Senior Data Scientist","58f6129fcae0fc4c":"Lead Data Scientist",
 "d1c4093738c41ea0":"Principal Data Scientist","a85ca41977af467e":"Product Data Scientist",
 "f1d2b17b0eda6de7":"Applied Data Scientist","00dd31da0bd5cab8":"Marketing Data Scientist",
 "a8585d2750f1df5c":"Research Data Scientist","6c9aa123bc61e556":"Junior Data Scientist",
 "cfe47eb3eee6effc":"Associate Data Scientist","717b04424edb79a4":"Data Science Intern"},
"ML Engineer": {
 "8ae98ef00eb1a9d3":"Machine Learning Engineer","15986ac54ed55b62":"Staff ML Engineer",
 "293dfff2319d0888":"Lead ML Engineer","e0c22e9b2f06b79d":"Applied ML Engineer",
 "63705b281e66ab21":"Principal ML Engineer","3b04f97539f15bee":"ML Platform Engineer",
 "0deb32909c99e419":"ML Systems Engineer","64089ff6561f84aa":"ML Software Engineer",
 "93c9e55495aaead6":"ML Infrastructure Engineer","3db30f4a4eb8c727":"ML Operations Engineer",
 "710b9ca3482e685a":"ML Architect","3f2131257658ee7e":"Senior Machine Learning Engineer",
 "e57a3879c93b317e":"Senior ML Engineer","0414e01327d6892a":"Machine Learning Developer",
 "21fe36994e34e3e0":"Deep Learning Engineer","5be1f6020e069dee":"MLops Engineer",
 "b2780fe4cdb85518":"Machine Learning Intern"},
"AI Engineer": {
 "dadf0773affc09e1":"AI Engineer","cd7d42fe7d795ab6":"Applied AI Engineer",
 "53ba176c0e716569":"AI/ML Engineer","d2e599d675c23776":"AI Software Engineer",
 "9daea98e285d5b0a":"AI Platform Engineer","457693f6b2f2c782":"Generative AI Engineer",
 "a927aac699135952":"Principal AI Engineer","2bacaf4fe87f5dde":"AI Product Engineer",
 "52f0d68fab37e829":"Forward Deployed AI Engineer","4733f2248f74706a":"AI Deployment Engineer",
 "6f5e89c60edd7bb5":"AI Infrastructure Engineer","3a4596ec50c598a5":"Staff AI Engineer",
 "c8d2350c015f664f":"AI Automation Engineer","5075dc31408c83c8":"Lead AI Engineer",
 "abaa542b62956459":"AI Security Engineer","c43a5af07aa35eef":"AI Agent Engineer",
 "46405704bbd5580d":"AI Data Engineer","034eb60e5df65709":"Senior AI Engineer",
 "7d981a3f95a404b1":"Artificial Intelligence Engineer","51e7984c9b32ed28":"Gen AI Engineer",
 "879c50da82459d2c":"GenAI Engineer","36b5108ea333419f":"LLM Engineer",
 "989ae78eb56d3cae":"AI Developer","da6c83934c17cd79":"Generative AI Developer",
 "8c92337412b3b8db":"AI/ML Developer"},
"AI Researcher": {
 "5c6fd4b038283bc8":"AI Researcher","10f9db43f6b96503":"AI Research Engineer",
 "8bcbc80692ba90f9":"Applied AI Researcher","de6941a406ab49fe":"AI Research Scientist",
 "7f99f5eb7720208a":"AI Scientist","50e9fca4fa8b072e":"Responsible AI Researcher",
 "710e1e74d4425561":"Embodied AI Researcher","5a0079898a87ff91":"AI Research Intern",
 "a490f771092d5778":"ML Researcher","80b890f766069cd2":"ML Scientist",
 "89f584a811c00c07":"ML Research Scientist","4fde55956a66229e":"ML Research Scientist 2",
 "83e656531d88c9f6":"ML Research Engineer","bc6846ee72461bd6":"ML Research Intern",
 "9d23b03b5c74b9f7":"Deep Learning Researcher","41f2fd72ee627d95":"AI/ML Research Scientist"},
}
import re
_AI   = r'(ai|a\.i|artificial intelligence|genai|gen ai|generative ai|llm)'
_ML   = r'(machine learning|ml|deep learning|dl)'
def family(title):
    """Raw-title -> family. Mirrors FAMILIES above (same IN/OUT rule)."""
    if not title: return None
    s = re.sub(r'[^a-z0-9+/. ]',' ', title.lower())
    s = re.sub(r'\s+',' ',s).strip()
    # OUT: distinct specialisations / advisory / adjacent roles -> never a family member
    if re.search(r'\b(computer vision|nlp|natural language|prompt engineer|ai consultant|ai specialist|'
                 r'applied scientist|data analyst|data engineer|business intelligence)\b', s): return None
    # researcher first (an "AI Research Engineer" is a researcher, not an AI engineer)
    if re.search(rf'\b{_AI}\b.*\b(research|researcher|scientist)\b', s) or \
       re.search(rf'\b{_ML}\b.*\b(research|researcher|scientist)\b', s) or \
       re.search(rf'\b(research|researcher)\b.*\b({_AI}|{_ML})\b', s): return 'AI Researcher'
    if re.search(rf'\b{_ML}\b.*\b(engineer|engineering|developer)\b', s) or re.search(r'\bmlops\b', s):
        return 'ML Engineer'
    if re.search(rf'\b{_AI}\b.*\b(engineer|engineering|developer)\b', s): return 'AI Engineer'
    if re.search(r'\bdata scientist\b|\bdata science\b', s): return 'Data Scientist'
    return None
FAMS = ['Data Scientist','ML Engineer','AI Engineer','AI Researcher']
