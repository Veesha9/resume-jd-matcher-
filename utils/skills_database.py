"""
skills_database.py
--------------------
A curated list of common tech + soft skills used to spot skill
mentions inside resume/JD text. This is intentionally a flat,
easy-to-extend Python list (not an ML model) so it's transparent,
fast, and simple to maintain — add new skills anytime as new
tools/frameworks become relevant to your field.
"""

SKILLS_DATABASE = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "sql",
    "r", "go", "rust", "php", "swift", "kotlin", "html", "css", "bash",

    # Data / ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data analysis", "data visualization", "data science",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "power bi", "tableau", "excel", "statistics", "a/b testing",
    "predictive modeling", "feature engineering",

    # Web / software dev
    "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
    "streamlit", "rest api", "graphql", "git", "github", "docker",
    "kubernetes", "ci/cd", "microservices", "agile", "scrum",

    # Cloud / infra
    "aws", "azure", "gcp", "google cloud", "linux", "devops",

    # Databases
    "mysql", "postgresql", "mongodb", "firebase", "redis",

    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "collaboration",
    "project management", "presentation", "adaptability",
    "attention to detail", "analytical skills",
]
