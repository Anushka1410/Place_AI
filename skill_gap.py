
# ==========================================
# PlaceAI - Skill Gap Analyzer
# ==========================================

def analyze_skill(skill, current_score, required_score):
    """Calculate skill gap, priority, and recommendation."""

    gap = required_score - current_score

    print(f"\nSkill: {skill}")
    print(f"Your level: {current_score}/100")
    print(f"Required level: {required_score}/100")

    if gap >= 30:
        print(f"Skill gap: {gap} points")
        print("Priority: HIGH")
        print(f"Recommendation: Practice {skill} daily.")

    elif gap > 0:
        print(f"Skill gap: {gap} points")
        print("Priority: MEDIUM")
        print(f"Recommendation: Improve your {skill} gradually.")

    else:
        print("Requirement achieved!")
        print("Priority: LOW")
        print(f"Recommendation: Keep practicing {skill}.")

def generate_roadmap(student_skills, required_skills):
    """Create a study roadmap based on skill gaps."""

    print("\n" + "=" * 40)
    print("       YOUR PERSONALIZED ROADMAP")
    print("=" * 40)

    # Sort skills by largest gap first
    skill_gaps = []

    for skill, target in required_skills.items():
        current = student_skills[skill]
        gap = max(target - current, 0)

        if gap > 0:
            skill_gaps.append((skill, gap))

    skill_gaps.sort(key=lambda item: item[1], reverse=True)

    if not skill_gaps:
        print("You've met all your current skill targets!")
        print("Keep practicing to maintain your skills.")
        return

    for position, (skill, gap) in enumerate(skill_gaps, start=1):
        print(f"{position}. Study {skill} - {gap} points to improve")

    print("\nStart with the skill that has the largest gap.")


def main():
    """Collect scores and generate the PlaceAI report."""

    # Target scores for a Python developer role
    required_skills = {
        "Python": 80,
        "SQL": 70,
        "Problem Solving": 75,
        "Git": 60
    }

    # Collect the student's current skill levels
    student_skills = {}

    print("=" * 40)
    print("          WELCOME TO PLACEAI")
    print("=" * 40)
    print("\nRate your current skills from 0 to 100.")

    for skill in required_skills:
        while True:
            try:
                score = int(input(f"Rate your {skill} skills: "))

                if 0 <= score <= 100:
                    student_skills[skill] = score
                    break
                else:
                    print("Please enter a score between 0 and 100.")

            except ValueError:
                print("Invalid input! Please enter a whole number.")

    # Generate the skill gap report
    print("\n" + "=" * 40)
    print("          YOUR SKILL GAP REPORT")
    print("=" * 40)

    report_lines = []

    total_score = 0
    total_required = 0

    for skill, required_score in required_skills.items():
        current_score = student_skills[skill]

        analyze_skill(skill, current_score, required_score)

        gap = required_score - current_score

        report_lines.append(
            f"{skill}: Your score = {current_score}/100, "
            f"Target = {required_score}/100, Gap = {max(gap, 0)}"
        )

        total_score += current_score
        total_required += required_score

    # Calculate average scores
    overall_score = total_score / len(student_skills)
    target_score = total_required / len(required_skills)
    generate_roadmap(student_skills, required_skills)

    # Display overall progress
    print("\n" + "=" * 40)
    print("          OVERALL PROGRESS")
    print("=" * 40)
    print(f"Your average skill score: {overall_score:.1f}/100")
    print(f"Average target score: {target_score:.1f}/100")

    # Show the average difference from the target
    difference = target_score - overall_score

    if difference > 0:
        print(f"Average score difference: {difference:.1f} points")
    else:
        print("Your average score meets or exceeds the average target!")
    report_lines.append(
        f"Overall average: {overall_score:.1f}/100"
    )

    with open("skill_report.txt", "a", encoding="utf-8") as file:
        file.write("\n--- New PlaceAI Report ---\n")

        for line in report_lines:
            file.write(line + "\n")

    print("\nYour report has been saved to skill_report.txt")
    print("\nKeep learning. You've got this!")
    print("=" * 40)


# Run the program
if __name__ == "__main__":
    main()
