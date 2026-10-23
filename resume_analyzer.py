
import re

# Skills PlaceAI can recognize
SKILL_KEYWORDS = {
    "Python": ["python"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "Git": ["git", "github", "gitlab"],
    "Machine Learning": [
        "machine learning", "scikit-learn", "sklearn"
    ],
    "Deep Learning": [
        "deep learning", "tensorflow", "pytorch", "keras"
    ],
    "Data Analysis": [
        "data analysis", "pandas", "numpy", "data analytics"
    ],
    "Artificial Intelligence": [
        "artificial intelligence", "ai", "generative ai"
    ],
    "Web Development": [
        "html", "css", "javascript", "fastapi", "flask", "django"
    ],
    "Data Visualization": [
        "matplotlib", "seaborn", "power bi", "tableau"
    ],
    "Cloud Computing": [
        "aws", "azure", "google cloud"
    ]
}


def extract_skills(resume_text):
    detected_skills = []

    # Ignore capitalization when matching
    text = resume_text.lower()

    for skill, keywords in SKILL_KEYWORDS.items():
        for keyword in keywords:
            # Match whole words/phrases, not accidental substrings
            pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

            if re.search(pattern, text):
                detected_skills.append(skill)
                break

    return detected_skills


def analyze_resume(resume_text):
    skills = extract_skills(resume_text)

    return {
        "detected_skills": skills,
        "total_skills_found": len(skills)
    }
