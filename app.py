from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO
from resume_analyzer import analyze_resume
from placement_roadmap import analyze_placement_gap
from typing import List
from urllib.parse import urlencode
from mock_interview import (
    generate_interview_questions,
    evaluate_answer
)


app = FastAPI(
    title="PlaceAI",
    description="Your AI-powered placement preparation assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Example target scores for a Python developer role
REQUIRED_SKILLS = {
    "Python": 80,
    "SQL": 70,
    "Problem Solving": 75,
    "Git": 60
}


# Validate scores submitted by the user
class SkillScores(BaseModel):
    python: int = Field(ge=0, le=100)
    sql: int = Field(ge=0, le=100)
    problem_solving: int = Field(ge=0, le=100)
    git: int = Field(ge=0, le=100)


@app.get("/")
def home():
    return {
        "message": "Welcome to PlaceAI!",
        "status": "Your placement preparation API is running."
    }


@app.get("/skills")
def get_skills():
    return REQUIRED_SKILLS


@app.post("/analyze")
def analyze_skills(scores: SkillScores):
    student_skills = {
        "Python": scores.python,
        "SQL": scores.sql,
        "Problem Solving": scores.problem_solving,
        "Git": scores.git
    }

    results = []
    total_score = 0
    total_target = 0

    for skill, target in REQUIRED_SKILLS.items():
        current = student_skills[skill]
        gap = max(target - current, 0)

        if gap >= 30:
            priority = "HIGH"
            recommendation = f"Practice {skill} daily."
        elif gap > 0:
            priority = "MEDIUM"
            recommendation = f"Improve your {skill} gradually."
        else:
            priority = "LOW"
            recommendation = f"Keep practicing {skill}."

        results.append({
            "skill": skill,
            "current_score": current,
            "target_score": target,
            "gap": gap,
            "priority": priority,
            "recommendation": recommendation
        })

        total_score += current
        total_target += target

    return {
        "skill_report": results,
        "average_skill_score": round(
            total_score / len(student_skills), 1
        ),
        "average_target_score": round(
            total_target / len(REQUIRED_SKILLS), 1
        )
    }


@app.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum size is 5 MB."
        )

    try:
        pdf = PdfReader(BytesIO(contents))

        if pdf.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Please upload an unlocked PDF."
            )

        extracted_text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        # Analyze the extracted resume text
        skill_report = analyze_resume(extracted_text)

        return {
            "filename": file.filename,
            "pages": len(pdf.pages),
            "detected_skills": skill_report["detected_skills"],
            "total_skills_found": skill_report["total_skills_found"],
            "message": "Resume analyzed successfully!"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not analyze this PDF. Please try another file."
        )
    finally:
        await file.close()

class PlacementRequest(BaseModel):
    detected_skills: List[str]


@app.post("/placement-roadmap")
def create_placement_roadmap(request: PlacementRequest):
    report = analyze_placement_gap(request.detected_skills)
    return report

# ---------- AI MOCK INTERVIEW ----------

class MockInterviewRequest(BaseModel):
    skills: List[str] = Field(min_length=1, max_length=10)
    difficulty: str = "Beginner"
    count: int = Field(default=5, ge=1, le=10)


class AnswerEvaluationRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    answer: str = Field(min_length=1, max_length=5000)
    skill: str = Field(min_length=1, max_length=100)


@app.post("/mock-interview/questions")
def create_mock_interview(request: MockInterviewRequest):
    questions = generate_interview_questions(
        skills=request.skills,
        difficulty=request.difficulty,
        count=request.count
    )

    return {
        "skills": request.skills,
        "difficulty": request.difficulty,
        "questions": questions
    }


@app.post("/mock-interview/evaluate")
def evaluate_mock_interview_answer(
    request: AnswerEvaluationRequest
):
    feedback = evaluate_answer(
        question=request.question,
        answer=request.answer,
        skill=request.skill
    )

    return {
        "skill": request.skill,
        "question": request.question,
        "feedback": feedback
    }

class JobSearchRequest(BaseModel):
    skills: List[str] = Field(min_length=1, max_length=50)
    location: str = "India"


@app.post("/job-matches")
def get_job_matches(request: JobSearchRequest):
    roles = [
        "AI/ML Engineer",
        "Python Developer",
        "Data Analyst",
    ]

    jobs = []

    for role in roles:
        search_query = f"{role} {' '.join(request.skills)}"
        params = urlencode({
            "keywords": search_query,
            "location": request.location,
        })

        jobs.append({
            "title": role,
            "location": request.location,
            "search_url": (
                "https://www.linkedin.com/jobs/search/?"
                + params
            ),
            "resume_skills": request.skills,
            "message": (
                "Open LinkedIn to explore current listings. "
                "Detailed resume-to-job matching will be added next."
            ),
        })

    return {
        "total": len(jobs),
        "jobs": jobs,
    }
