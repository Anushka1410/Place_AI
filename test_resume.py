from resume_analyzer import analyze_resume

sample_resume = """
B.Tech Computer Science student.
Skills: Python, SQL, Git, Machine Learning,
Pandas, NumPy, TensorFlow, FastAPI.
Projects: AI placement preparation platform.
"""

result = analyze_resume(sample_resume)

print("Resume Analysis Report")
print("----------------------")
print("Detected Skills:", result["detected_skills"])
print("Total Skills Found:", result["total_skills_found"])