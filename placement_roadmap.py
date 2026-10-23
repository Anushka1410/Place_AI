
# placement_roadmap.py

# Skills expected for an entry-level AI/ML placement role
JOB_REQUIREMENTS = {
    "Python": {
        "priority": "HIGH",
        "topics": [
            "Functions, lists and dictionaries",
            "File handling and exception handling",
            "Coding problems using Python"
        ],
        "duration": 1
    },
    "SQL": {
        "priority": "HIGH",
        "topics": [
            "SELECT, WHERE and ORDER BY",
            "GROUP BY and aggregate functions",
            "JOINs and subqueries"
        ],
        "duration": 1
    },
    "Problem Solving": {
        "priority": "HIGH",
        "topics": [
            "Arrays and strings",
            "Searching and sorting",
            "Easy coding problems"
        ],
        "duration": 1
    },
    "Machine Learning": {
        "priority": "HIGH",
        "topics": [
            "Supervised and unsupervised learning",
            "Regression and classification",
            "Model evaluation and scikit-learn"
        ],
        "duration": 1
    },
    "Data Analysis": {
        "priority": "MEDIUM",
        "topics": [
            "NumPy and Pandas",
            "Data cleaning",
            "Exploratory data analysis"
        ],
        "duration": 1
    },
    "Git": {
        "priority": "MEDIUM",
        "topics": [
            "Git add, commit and push",
            "Branches and merging",
            "GitHub repositories"
        ],
        "duration": 1
    },
    "Deep Learning": {
        "priority": "MEDIUM",
        "topics": [
            "Neural network fundamentals",
            "TensorFlow or PyTorch basics",
            "Build a small deep learning project"
        ],
        "duration": 1
    },
    "Artificial Intelligence": {
        "priority": "MEDIUM",
        "topics": [
            "AI fundamentals",
            "Search and reasoning basics",
            "Explore a small AI application"
        ],
        "duration": 1
    },
    "Web Development": {
        "priority": "MEDIUM",
        "topics": [
            "HTML and CSS fundamentals",
            "JavaScript basics",
            "Build a small web application"
        ],
        "duration": 1
    },
    "Data Visualization": {
        "priority": "LOW",
        "topics": [
            "Matplotlib basics",
            "Create charts from datasets",
            "Present insights clearly"
        ],
        "duration": 1
    },
    "Cloud Computing": {
        "priority": "LOW",
        "topics": [
            "Cloud computing fundamentals",
            "Explore a cloud platform",
            "Learn basic deployment"
        ],
        "duration": 1
    }
}


def analyze_placement_gap(detected_skills):
    # Normalize skill names for reliable comparison
    normalized_skills = {
        skill.strip().casefold()
        for skill in detected_skills
        if isinstance(skill, str)
    }

    matched_skills = []
    missing_skills = []

    for skill, details in JOB_REQUIREMENTS.items():
        if skill.casefold() in normalized_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append({
                "skill": skill,
                "priority": details["priority"],
                "topics": details["topics"],
                "duration_weeks": details["duration"]
            })

    total_required = len(JOB_REQUIREMENTS)
    match_percentage = round(
        len(matched_skills) / total_required * 100
    )

    # Put high-priority gaps first
    priority_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    missing_skills.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    # Create a four-week starter roadmap
    roadmap = []

    for week, item in enumerate(missing_skills[:4], start=1):
        roadmap.append({
            "week": week,
            "focus_skill": item["skill"],
            "priority": item["priority"],
            "topics": item["topics"],
            "goal": (
                f"Study {item['skill']} fundamentals and "
                "complete at least one practical exercise."
            )
        })

    return {
        "target_role": "Entry-Level AI/ML",
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": total_required,
        "total_matched_skills": len(matched_skills),
        "match_percentage": match_percentage,
        "learning_roadmap": roadmap,
        "note": (
            "This is a keyword-based estimate against a starter "
            "skill profile, not a guarantee of job readiness."
        )
    }
