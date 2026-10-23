
from placement_roadmap import analyze_placement_gap

resume_skills = [
    "Python",
    "SQL",
    "Git"
]

report = analyze_placement_gap(resume_skills)

print("Target Role:", report["target_role"])
print("Profile Match:", str(report["match_percentage"]) + "%")
print("Matched Skills:", report["matched_skills"])

print("\nMissing Skills:")
for item in report["missing_skills"]:
    print(f"- {item['skill']} ({item['priority']} priority)")

print("\nPersonalized Learning Roadmap:")
for week in report["learning_roadmap"]:
    print(f"\nWeek {week['week']}: {week['focus_skill']}")
    for topic in week["topics"]:
        print("  -", topic)
