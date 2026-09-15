"""Classifier for the full tech-role leaderboard.
CORE 21 = the roles from the 2026 pay analysis (kept verbatim so the race lines
up with that post). ERA = period-appropriate roles added so the 1990s/2000s are
not an artificially empty screen - omitting them would be the classic
'modern instrument applied to the past' error, which fakes a universal rise.
Order matters: first match wins, most specific first."""
import re
RULES = [
 # --- AI / ML / data (modern) ---
 ("AI Engineer",            r"\b(ai|a\.i|artificial intelligence|genai|gen ai|generative ai|llm)\b[\w /]*\b(engineer|developer)\b"),
 ("ML Engineer",            r"\b(machine learning|ml|deep learning)\b[\w /]*\b(engineer|developer)\b|\bmlops\b"),
 ("Research Scientist",     r"\bresearch scientist\b|\bresearch engineer\b|\b(ai|ml|machine learning)\b[\w /]*\bresearch(er)?\b|\bapplied scientist\b"),
 ("Data Scientist",         r"\bdata scientist\b|\bdata science\b"),
 ("Data Engineer",          r"\bdata engineer\b|\banalytics engineer\b|\betl (developer|engineer)\b|\bbig data engineer\b"),
 ("Data Analyst",           r"\bdata analyst\b|\banalytics analyst\b|\bbusiness intelligence analyst\b|\bbi analyst\b|\breporting analyst\b"),
 ("Database Administrator", r"\bdatabase administrator\b|\bdba\b|\bdatabase engineer\b"),
 # --- cloud / infra / ops ---
 ("Site Reliability Engineer", r"\bsite reliability\b|\bsre\b"),
 ("DevOps Engineer",        r"\bdevops\b|\bdev ops\b"),
 ("Platform Engineer",      r"\bplatform engineer\b|\bplatform engineering\b"),
 ("Cloud Engineer",         r"\bcloud (engineer|architect|consultant|specialist)\b|\baws (engineer|architect)\b|\bazure (engineer|architect)\b"),
 ("Infrastructure Engineer",r"\binfrastructure engineer\b|\bsystems administrator\b|\bsysadmin\b|\bsystem administrator\b"),
 ("Network Engineer",       r"\bnetwork (engineer|administrator|architect)\b"),
 ("Security Engineer",      r"\b(security|cyber ?security|infosec|information security)\b[\w /]*\b(engineer|analyst|architect|specialist)\b"),
 # --- software ---
 ("Frontend Engineer",      r"\bfront.?end\b[\w /]*\b(engineer|developer)\b|\bui (engineer|developer)\b"),
 ("Backend Engineer",       r"\bback.?end\b[\w /]*\b(engineer|developer)\b"),
 ("Full Stack Engineer",    r"\bfull.?stack\b"),
 ("Mobile Engineer",        r"\b(ios|android|mobile)\b[\w /]*\b(engineer|developer)\b"),
 ("Web Developer",          r"\bweb (developer|programmer)\b|\bwebmaster\b|\bweb designer\b"),
 ("QA / SDET Engineer",     r"\b(qa|quality assurance|software test|test automation|quality engineer)\b[\w /]*\b(engineer|analyst|lead|specialist|manager)\b|\bsdet\b|\bsoftware development engineer in test\b|\b(software |automation )?tester\b|\bqa\b$"),
 ("Systems Engineer",       r"\bsystems? engineer\b"),
 ("Software Engineer",      r"\bsoftware (engineer|developer|architect)\b|\bsde\b|\bprogrammer\b|\bapplication developer\b|\bsoftware development engineer\b|\bdeveloper\b"),
 # --- product / design / analysis ---
 ("Product Manager",        r"\bproduct manager\b|\bproduct owner\b|\bproduct management\b"),
 ("Product Designer",       r"\bproduct designer\b|\bux (designer|researcher)\b|\bui/ux\b|\buser experience\b|\binteraction designer\b"),
 ("Product Engineer",       r"\bproduct engineer\b"),
 ("Business Analyst",       r"\bbusiness analyst\b|\bsystems analyst\b|\bbusiness systems analyst\b"),
 ("Project / Program Manager", r"\btechnical program manager\b|\btpm\b|\bprogram manager\b|\bproject manager\b|\bscrum master\b|\bdelivery manager\b"),
 ("IT Support",             r"\b(it|help ?desk|desktop|technical) support\b|\bit technician\b|\bsupport engineer\b|\bsupport specialist\b"),
 ("Solutions Architect",    r"\bsolutions? architect\b|\bsolutions? engineer\b|\bsales engineer\b|\bpre.?sales\b"),
 ("Technical Writer",       r"\btechnical writer\b|\bdocumentation specialist\b"),
]
RULES=[(n,re.compile(p,re.I)) for n,p in RULES]
CORE21={"Research Scientist","ML Engineer","Product Engineer","AI Engineer","Backend Engineer",
 "Frontend Engineer","Software Engineer","Infrastructure Engineer","Security Engineer","Product Manager",
 "Platform Engineer","Site Reliability Engineer","Full Stack Engineer","Product Designer","Data Scientist",
 "DevOps Engineer","Data Engineer","Systems Engineer","QA / SDET Engineer","Data Analyst","Business Analyst"}

GROUP={
 # 4 chromatic groups + 1 neutral. Five chromatic slots cannot clear the
 # all-pairs colour floors (validated), and bars reorder every frame, so
 # all-pairs is the governing case. Security folds into Infrastructure.
 "AI Engineer":"AI & ML","ML Engineer":"AI & ML","Research Scientist":"AI & ML",
 "Data Scientist":"Data","Data Engineer":"Data","Data Analyst":"Data","Database Administrator":"Data",
 "Site Reliability Engineer":"Infrastructure & Security","DevOps Engineer":"Infrastructure & Security",
 "Platform Engineer":"Infrastructure & Security","Cloud Engineer":"Infrastructure & Security",
 "Infrastructure Engineer":"Infrastructure & Security","Network Engineer":"Infrastructure & Security",
 "Security Engineer":"Infrastructure & Security",
 "Frontend Engineer":"Software","Backend Engineer":"Software","Full Stack Engineer":"Software",
 "Mobile Engineer":"Software","Web Developer":"Software","Software Engineer":"Software",
 "Systems Engineer":"Software","QA / SDET Engineer":"Software",
 "Product Manager":"Product & Business","Product Designer":"Product & Business",
 "Product Engineer":"Product & Business","Business Analyst":"Product & Business",
 "Project / Program Manager":"Product & Business","IT Support":"Product & Business",
 "Solutions Architect":"Product & Business","Technical Writer":"Product & Business",
}

MGMT=re.compile(r"\b(director|vp|vice president|chief|cto|ceo|head of|president|partner|owner|founder)\b",re.I)
def role_of(title):
    if not title: return None
    if MGMT.search(title): return None          # exec/management track, not an IC role
    for n,p in RULES:
        if p.search(title): return n
    return None
