"""Named technologies vs generic capabilities.

The distinction the race turns on. A NAMED TECHNOLOGY is a specific artifact
someone ships and someone else adopts -- a language, product, framework,
platform or service with a proprietor or a formal specification. A CAPABILITY
is an activity you perform, which any number of tools could carry out.

The test applied to each term: *could this have a version number and an owner?*
Docker 24.0 from Docker Inc., yes. "troubleshooting", no.

Hand-assigned, because there is no field in the data that encodes it and a
heuristic on the string cannot tell "Jira" from "testing". Every term that ever
reaches 0.5% of a trailing-twelve-month window is assigned, and `audit()` prints
anything above that line that was missed, so the list cannot silently omit a
term that belongs in the race.

Borderline calls, made explicitly rather than quietly:
  * SQL       -> NAMED. An ANSI specification, and in practice a concrete
                 dialect people list as a tool.
  * REST APIs -> capability. An architectural style with no owner.
  * CI/CD     -> capability. A practice; Jenkins and GitHub Actions are the
                 named things that carry it out, and both are listed separately.
  * ETL       -> capability, same reason (SSIS, Airflow, dbt are the artifacts).
  * LLMs      -> NAMED, reluctantly. It is a class rather than one product, but
                 it is a thing you adopt, not an activity you perform, and
                 excluding it would blind the race to the AI wave entirely.
                 Flagged in the writeup as a judgement call.
  * Machine learning -> capability. The field, not an artifact.
"""
from __future__ import annotations

NAMED: set[str] = set()
CAPABILITY: set[str] = set()


def _n(*xs: str) -> None:
    NAMED.update(xs)


def _c(*xs: str) -> None:
    CAPABILITY.update(xs)


# Languages and runtimes.
_n("Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "PHP", "Perl",
   "Ruby", "Go", "Scala", "Kotlin", "Swift", "Rust", "R", "MATLAB", "COBOL",
   "Visual Basic", "VBA", "Objective-C", "Groovy", "Assembly", "Fortran",
   ".NET", "ASP.NET", "ASP", "JSP", "J2EE", "PL/SQL", "T-SQL", "Bash",
   "PowerShell", "Shell scripting", "SAS", "SPSS", "Delphi", "PowerBuilder")
# Data stores, query languages and analytics products.
_n("SQL", "MySQL", "PostgreSQL", "SQL Server", "Oracle", "Db2", "Sybase",
   "MongoDB", "Redis", "Cassandra", "Teradata", "MS Access", "Snowflake",
   "Databricks", "Redshift", "BigQuery", "Hadoop", "Spark", "Kafka", "Airflow",
   "dbt", "SSIS", "SSRS", "Excel", "Tableau", "Power BI", "Looker", "Qlik",
   "Elasticsearch", "Informatica", "Crystal Reports")
# Web and application frameworks.
_n("HTML", "CSS", "React", "Angular", "Vue.js", "jQuery", "Node.js", "XML",
   "Bootstrap", "Django", "Flask", "Rails", "Spring", "Spring Boot", "Struts",
   "WebSphere", "ColdFusion", "Flash", "Silverlight", "AJAX", "Next.js",
   "React Native", "Webpack", "Sass", "GraphQL", "JSON", "Servlets", "Figma")
# Operating systems, infrastructure, cloud and tooling.
_n("Linux", "Unix", "Solaris", "Windows", "Windows NT", "Windows Server",
   "AWS", "Azure", "GCP", "S3", "EC2", "Docker", "Kubernetes", "Jenkins",
   "Terraform", "Ansible", "Puppet", "Chef", "Git", "GitHub", "GitLab",
   "GitHub Actions", "Azure DevOps", "Subversion", "Active Directory",
   "VMware", "Citrix", "Novell", "Cisco", "Apache", "IIS", "Nginx", "TCP/IP",
   "SharePoint", "Salesforce", "SAP", "Jira", "Confluence", "ServiceNow",
   "Splunk", "Datadog", "Selenium", "Postman")
# AI/ML artifacts.
_n("TensorFlow", "PyTorch", "scikit-learn", "pandas", "NumPy", "LLMs",
   "LangChain", "OpenAI", "Hugging Face")

# Activities, methods and roles-of-work -- no owner, no version number.
_c("testing", "test cases", "test plans", "Quality Assurance", "QA",
   "documentation", "training", "troubleshooting", "maintenance",
   "implementation", "design", "project management", "requirements gathering",
   "data analysis", "dashboards", "reporting", "reports", "Customer service",
   "customer service", "compliance", "Compliance", "automation", "leadership",
   "communication", "code review", "Agile", "Scrum", "Waterfall", "SDLC",
   "UAT", "ITIL", "ETL", "CI/CD", "CI/CD pipelines", "REST APIs", "APIs",
   "Machine learning", "Deep learning", "data science", "statistics",
   "NLP", "computer vision", "predictive modeling", "MLOps", "networking",
   "stored procedures", "data warehousing", "prompt engineering", "RAG",
   "Generative AI", "AI", "security", "architecture", "mentoring",
   "incident response", "budgeting", "forecasting", "SEO", "analysis",
   "development", "support", "integration", "migration", "optimization",
   "configuration", "deployment", "monitoring", "scripting", "debugging")


def kind(label: str) -> str:
    if label in NAMED:
        return "named"
    if label in CAPABILITY:
        return "capability"
    return "unassigned"


def audit(concepts) -> list[str]:
    """Terms in the race pool that nobody classified. Must be empty to ship."""
    return [c for c in concepts if kind(c) == "unassigned"]
