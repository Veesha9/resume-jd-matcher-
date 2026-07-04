"""
matcher.py
-----------
Core NLP logic for comparing a resume against a job description.

Two things happen here:
1. Overall similarity score — using TF-IDF vectors + cosine similarity.
   This tells you *how close in content* the two documents are overall,
   the same core technique used by real resume-screening tools (ATS).
2. Skill-level gap analysis — a simple, transparent keyword match
   against a curated skills list, so you can literally see which
   skills the JD mentions that your resume doesn't.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.skills_database import SKILLS_DATABASE


def compute_match_score(resume_text: str, jd_text: str) -> float:
    """
    Returns a 0-100 similarity score between resume and job description
    using TF-IDF vectorization + cosine similarity.

    TF-IDF turns each document into a vector of "how important is each
    word to this document relative to the other document." Cosine
    similarity then measures the angle between those two vectors —
    1.0 means identical content direction, 0 means totally unrelated.
    """
    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 1)


def extract_skills(text: str, skills_db=SKILLS_DATABASE) -> set:
    """
    Finds which skills from `skills_db` appear in `text`.
    Uses word-boundary regex matching so "r" doesn't falsely match
    inside "framework", and multi-word skills like "machine learning"
    are matched as a whole phrase.
    """
    text_lower = text.lower()
    found = set()

    for skill in skills_db:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)

    return found


def get_skill_gap(resume_text: str, jd_text: str) -> dict:
    """
    Compares skills mentioned in the JD vs the resume.

    Returns a dict with:
      - matched: skills present in both (your strengths for this role)
      - missing: skills the JD wants but your resume doesn't mention
      - resume_only: skills you have that the JD didn't ask for (bonus)
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    return {
        "matched": sorted(resume_skills & jd_skills),
        "missing": sorted(jd_skills - resume_skills),
        "resume_only": sorted(resume_skills - jd_skills),
    }
