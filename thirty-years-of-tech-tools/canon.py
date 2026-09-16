"""Canonicalise resolved skill entities into concepts, and group them for display.

Two separate jobs, deliberately kept apart:

  * MERGE  -- the entity resolver emits case/punctuation/acronym variants of the
    same concept (SKI-165): `python`/`Python`, `MYSQL`/`MySQL`, `ci/cd`/`CI/CD`.
    Merging is a data-quality fix and is applied to ENTITY IDS, so the merged
    position count is recomputed server-side as a DISTINCT over positions --
    summing per-variant counts would double-count a position naming two variants.

  * GROUP  -- assigning a concept to a display family (Languages, Data & BI, ...)
    is a presentation choice. It is hand-written for the top concepts only, each
    with a visible rule, because the race needs a stable colour per bar. Anything
    unassigned falls to "Other" rather than being guessed.
"""
from __future__ import annotations
import re

# Never merged: short names whose case/punctuation IS the identity.
PROTECTED = {"c", "c++", "c#", "r", "go", "d", "f#", ".net", "j2ee"}


def norm(s: str) -> str:
    """Normalisation key for merging. Preserves + and # so C/C++/C# stay apart."""
    s = (s or "").strip()
    bare = re.sub(r"\s*\([^)]*\)\s*$", "", s).strip()
    t = (bare if len(bare) >= 2 else s).lower()
    t = re.sub(r"[-_/.]+", " ", t)
    t = re.sub(r"[^\w\s+#]", "", t)
    return re.sub(r"\s+", " ", t).strip()


# Hand aliases where normalisation alone does not join two spellings of one
# concept. Keys are norm() output; values are the concept label.
ALIAS = {
    "js": "JavaScript", "javascript": "JavaScript", "ecmascript": "JavaScript",
    "node js": "Node.js", "nodejs": "Node.js", "node": "Node.js",
    "reactjs": "React", "react js": "React", "react native": "React Native",
    "angularjs": "Angular", "angular js": "Angular", "vuejs": "Vue.js", "vue": "Vue.js",
    "postgres": "PostgreSQL", "postgresql": "PostgreSQL",
    "mysql": "MySQL", "ms sql server": "SQL Server", "mssql": "SQL Server",
    "sql server": "SQL Server", "tsql": "T-SQL", "t sql": "T-SQL", "plsql": "PL/SQL",
    "oracle": "Oracle", "oracle database": "Oracle",
    "amazon web services": "AWS", "aws": "AWS", "aws cloud": "AWS",
    "microsoft azure": "Azure", "azure": "Azure",
    "google cloud platform": "GCP", "gcp": "GCP", "google cloud": "GCP",
    "k8s": "Kubernetes", "kubernetes": "Kubernetes",
    "ci cd": "CI/CD", "cicd": "CI/CD", "continuous integration": "CI/CD",
    "ms excel": "Excel", "microsoft excel": "Excel", "excel": "Excel",
    "powerbi": "Power BI", "power bi": "Power BI",
    "machine learning": "Machine learning", "ml": "Machine learning",
    "deep learning": "Deep learning",
    "html5": "HTML", "html": "HTML", "css3": "CSS", "css": "CSS",
    "dotnet": ".NET", " net": ".NET", "net": ".NET", "asp net": "ASP.NET",
    "visual basic": "Visual Basic", "vb": "Visual Basic", "vba": "VBA",
    "objective c": "Objective-C", "golang": "Go",
    "scikit learn": "scikit-learn", "sklearn": "scikit-learn",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch",
    "unix": "Unix", "linux": "Linux",
    "windows server": "Windows Server", "microsoft windows": "Windows",
    "etl": "ETL", "sql": "SQL", "nosql": "NoSQL",
    "rest api": "REST APIs", "rest apis": "REST APIs", "restful apis": "REST APIs",
    "rest": "REST APIs", "api": "APIs", "apis": "APIs",
    "llm": "LLMs", "llms": "LLMs", "large language models": "LLMs",
    "generative ai": "Generative AI", "genai": "Generative AI",
    "artificial intelligence": "AI",
}

# Display families for the race. Rule for each is in the comment; anything not
# listed is "Other" and is not colour-coded as if we knew what it was.
GROUP: dict[str, str] = {}


def _g(family: str, *names: str) -> None:
    for n in names:
        GROUP[n] = family


# General-purpose programming languages.
_g("Languages", "Java", "JavaScript", "Python", "C", "C++", "C#", "PHP", "Perl",
   "Ruby", "Go", "Scala", "TypeScript", "Visual Basic", "VBA", "Objective-C",
   "Swift", "Kotlin", "Rust", "R", "MATLAB", "COBOL", "Assembly", "Groovy",
   ".NET", "ASP.NET", "J2EE")
# Databases and the query languages bound to them.
_g("Data & BI", "SQL", "MySQL", "PostgreSQL", "SQL Server", "Oracle", "T-SQL",
   "PL/SQL", "NoSQL", "MongoDB", "ETL", "Excel", "Tableau", "Power BI",
   "data analysis", "stored procedures", "dashboards", "Hadoop", "Spark",
   "Snowflake", "Redshift", "Databricks", "dbt", "Airflow", "SSIS", "SSRS",
   "Access", "data warehousing", "Teradata", "BigQuery", "Looker", "Qlik")
# Browser-side and the frameworks that render into it.
_g("Web & frontend", "HTML", "CSS", "React", "Angular", "Vue.js", "jQuery",
   "Node.js", "Bootstrap", "XML", "ASP", "ColdFusion", "Flash", "Silverlight",
   "Django", "Flask", "Rails", "Spring Boot", "Spring", "REST APIs", "APIs",
   "React Native", "Next.js", "Webpack", "Sass", "AJAX", "JSP", "Servlets")
# Where code runs and how it gets there.
_g("Infra & cloud", "Linux", "Unix", "Windows", "Windows Server", "AWS", "Azure",
   "GCP", "Kubernetes", "Docker", "Jenkins", "Terraform", "CI/CD", "Git",
   "Ansible", "Puppet", "Chef", "Active Directory", "VMware", "Cisco", "TCP/IP",
   "S3", "EC2", "Lambda", "networking", "Bash", "PowerShell", "Shell scripting",
   "Apache", "IIS", "Nginx", "Novell", "Citrix", "SharePoint")
# Statistical and learned models, and the tools specific to them.
_g("AI & ML", "Machine learning", "Deep learning", "TensorFlow", "PyTorch",
   "scikit-learn", "NLP", "computer vision", "LLMs", "Generative AI", "AI",
   "pandas", "NumPy", "data science", "statistics", "predictive modeling",
   "RAG", "prompt engineering", "LangChain", "MLOps")
# How the work is organised, rather than what it is built with.
_g("Practices", "Agile", "Scrum", "Jira", "testing", "test cases", "test plans",
   "documentation", "project management", "troubleshooting", "training",
   "automation", "requirements gathering", "QA", "code review", "Confluence",
   "reporting", "reports", "customer service", "compliance", "design",
   "leadership", "communication", "Waterfall", "SDLC", "UAT", "ITIL")


# Display casing for proper nouns whose MODAL spelling in the corpus is
# lowercase. Applied only to the label, never to the grouping, so it cannot
# change which entities merge -- purely how the concept is printed.
DISPLAY = {
    "python": "Python", "docker": "Docker", "kubernetes": "Kubernetes",
    "terraform": "Terraform", "oracle": "Oracle", "linux": "Linux",
    "mysql": "MySQL", "postgresql": "PostgreSQL", "git": "Git",
    "jenkins": "Jenkins", "ansible": "Ansible", "kafka": "Kafka",
    "spark": "Spark", "hadoop": "Hadoop", "django": "Django", "flask": "Flask",
    "numpy": "NumPy", "pandas": "pandas", "matlab": "MATLAB", "perl": "Perl",
    "ruby": "Ruby", "swift": "Swift", "kotlin": "Kotlin", "scala": "Scala",
    "php": "PHP", "bash": "Bash", "powershell": "PowerShell", "unix": "Unix",
    "apache": "Apache", "nginx": "Nginx", "windows": "Windows", "azure": "Azure",
    "jira": "Jira", "tableau": "Tableau", "excel": "Excel", "agile": "Agile",
    "scrum": "Scrum", "salesforce": "Salesforce", "sharepoint": "SharePoint",
    "mongodb": "MongoDB", "redis": "Redis", "graphql": "GraphQL",
    "typescript": "TypeScript", "javascript": "JavaScript", "html": "HTML",
    "css": "CSS", "xml": "XML", "json": "JSON", "sql": "SQL", "etl": "ETL",
    "api": "APIs", "rest": "REST APIs", "saas": "SaaS", "cobol": "COBOL",
    "flash": "Flash", "coldfusion": "ColdFusion", "silverlight": "Silverlight",
    "jquery": "jQuery", "angular": "Angular", "react": "React", "vue": "Vue.js",
    "snowflake": "Snowflake", "databricks": "Databricks", "airflow": "Airflow",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "novell": "Novell",
    "citrix": "Citrix", "vmware": "VMware", "cisco": "Cisco",
}


def display(label: str) -> str:
    """Prettify a concept label without changing the grouping it came from."""
    return DISPLAY.get(label.strip().lower(), label)


def concept(name: str) -> str:
    """Map one resolved canonical_name to its merged concept label."""
    n = norm(name)
    if not n:
        return ""
    if n in PROTECTED:
        return {"c": "C", "c++": "C++", "c#": "C#", "r": "R", "go": "Go",
                "f#": "F#", ".net": ".NET", "j2ee": "J2EE", "d": "D"}[n]
    return ALIAS.get(n, name.strip())


def family(label: str) -> str:
    return GROUP.get(label, "Other")
