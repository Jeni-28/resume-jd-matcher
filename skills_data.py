"""
A simple predefined skills database for the Resume vs JD Matcher project.
Feel free to expand this list with more skills relevant to your target roles.
"""

SKILLS_DB = [
    # Programming languages
    "python", "sql", "r", "java", "c++", "c#", "javascript", "scala",

    # Data analysis / BI tools
    "excel", "power bi", "tableau", "looker", "google sheets", "ssrs",

    # Python libraries
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "scipy",
    "plotly", "statsmodels",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "nosql",
    "data warehousing", "etl",

    # Machine learning / AI
    "machine learning", "deep learning", "nlp", "llm", "rag",
    "tensorflow", "pytorch", "keras", "regression", "classification",
    "clustering", "time series", "feature engineering",

    # Cloud / Big data
    "aws", "azure", "gcp", "spark", "hadoop", "databricks", "snowflake",

    # Soft / analytical skills
    "data visualization", "data cleaning", "statistics", "a/b testing",
    "hypothesis testing", "dashboarding", "data storytelling",
    "problem solving", "communication", "stakeholder management",

    # Tools
    "git", "github", "jira", "airflow", "docker", "streamlit",
]

# ---------------------------------------------------------
# SYNONYMS
# ---------------------------------------------------------
# Maps alternate phrasings to the canonical skill name used in SKILLS_DB.
# This lets the matcher recognize "Amazon Web Services" as "aws", or
# "data viz" as "data visualization", instead of requiring exact wording.
SKILL_SYNONYMS = {
    "aws": ["amazon web services"],
    "gcp": ["google cloud", "google cloud platform"],
    "azure": ["microsoft azure"],
    "data visualization": ["data viz", "visualizing data", "dashboards and visualizations", "visualization"],
    "data cleaning": ["data cleansing", "data wrangling", "cleaning datasets"],
    "data warehousing": ["data warehouse", "data warehouses"],
    "etl": ["extract transform load", "etl pipelines", "etl processes"],
    "stakeholder management": ["stakeholders", "cross-functional teams", "cross functional collaboration"],
    "communication": ["communication skills", "verbal and written communication"],
    "machine learning": ["ml models", "ml"],
    "nlp": ["natural language processing"],
    "sql": ["structured query language"],
    "power bi": ["powerbi", "power-bi"],
    "a/b testing": ["ab testing", "split testing"],
    "hypothesis testing": ["statistical testing"],
}
