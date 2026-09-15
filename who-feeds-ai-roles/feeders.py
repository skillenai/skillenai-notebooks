"""Canonical feeder-title normaliser for the raw-profile path.
The API path is entity-resolved; this reconstructs comparable labels from raw
titles so the monthly series can be validated against the annual resolved one."""
import re
SEN=re.compile(r'^(sr\.?|senior|jr\.?|junior|staff|lead|principal|chief|head of|associate|assistant|'
 r'entry.level|mid.level|intermediate|apprentice|trainee|graduate|student|summer|contract|freelance|'
 r'i{1,3}|iv|v|1|2|3|4)\b[\s\-,]*',re.I)
TAIL=re.compile(r'\s*[\(\[,|@\-–—/].*$')
RULES=[
 ('Research Assistant',   r'research assistant|graduate research assistant|research asst'),
 ('Teaching Assistant',   r'teaching assistant|graduate teaching assistant|teaching asst'),
 ('Research Intern',      r'research intern'),
 ('Research Scientist',   r'research scientist'),
 ('Researcher',           r'^researcher$|^academic researcher$|^postdoc|postdoctoral'),
 ('Research Associate',   r'research associate|research fellow'),
 ('Professor / Lecturer', r'professor|lecturer|instructor|faculty'),
 ('Data Analyst',         r'data analyst|analytics analyst|reporting analyst'),
 ('Business Analyst',     r'business analyst|business intelligence analyst|\bbi analyst'),
 ('Data Engineer',        r'data engineer|analytics engineer|etl developer'),
 ('Software Engineer',    r'software engineer|software developer|\bsde\b|full.?stack|backend|back.end|'
                          r'frontend|front.end|web developer|programmer|software architect|application developer'),
 ('Product Manager',      r'product manager|product owner'),
 ('Project Manager',      r'project manager|program manager|scrum master|delivery manager'),
 ('Consultant',           r'consultant|advisory'),
 ('Financial Analyst',    r'financial analyst|finance analyst|investment analyst|quantitative analyst|\bquant\b'),
 ('Statistician',         r'statistician|biostatistician'),
 ('Intern',               r'^intern$|^internship$|\bintern\b'),
]
RULES=[(n,re.compile(p,re.I)) for n,p in RULES]
def canon_feeder(title, fam_fn):
    """AI families keep their family name; everything else maps to a canonical feeder."""
    if not title: return None
    f=fam_fn(title)
    if f: return f
    t=TAIL.sub('',title.strip()); 
    for _ in range(3):
        t2=SEN.sub('',t)
        if t2==t: break
        t=t2
    t=re.sub(r'\s+',' ',t).strip()
    for n,p in RULES:
        if p.search(title): return n
    return 'All other roles'
