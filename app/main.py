import os
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import ChildProfile, GradeLevel, SkillDomain, CustomGenerateRequest
from app.curriculum import (
    get_all_curriculum_nodes, get_lesson_plan, compute_skills_status,
    CURRICULUM_SKILLS
)
from app.storage import (
    get_profile, save_profile, save_submission, get_all_submissions,
    save_custom_lesson, get_custom_lesson, UPLOADS_DIR
)
from app.agent import teacher_agent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="Junior Kindergarten to Elementary AI Teacher Agent")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded worksheet photos
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
# Serve static frontend assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/profile")
async def fetch_profile():
    profile = get_profile()
    skills_status = compute_skills_status(profile.mastered_skills, profile.grade)
    
    # Calculate stats
    total_in_grade = sum(1 for s in skills_status.values() if s["grade"] == profile.grade)
    mastered_in_grade = sum(1 for s in skills_status.values() if s["grade"] == profile.grade and s["status"] == "mastered")
    
    return {
        "profile": profile,
        "grade_stats": {
            "total": total_in_grade,
            "mastered": mastered_in_grade,
            "percent": int((mastered_in_grade / total_in_grade * 100) if total_in_grade else 0)
        }
    }

@app.post("/api/profile")
async def update_profile(profile_data: ChildProfile):
    save_profile(profile_data)
    return {"status": "ok", "profile": profile_data}

@app.get("/api/curriculum")
async def fetch_curriculum(grade: str = None):
    profile = get_profile()
    skills_status = compute_skills_status(profile.mastered_skills, profile.grade)
    
    nodes = list(skills_status.values())
    if grade:
        nodes = [n for n in nodes if n["grade"] == grade]
        
    return {
        "current_grade": profile.grade,
        "nodes": nodes
    }

@app.get("/api/lessons/{lesson_id}")
async def fetch_lesson(lesson_id: str):
    # Check custom lessons first
    if lesson_id.startswith("custom_"):
        lesson = get_custom_lesson(lesson_id)
        if lesson:
            return lesson
            
    lesson = get_lesson_plan(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@app.post("/api/lessons/generate")
async def generate_custom_worksheet(req: CustomGenerateRequest):
    profile = get_profile()
    if not req.child_name:
        req.child_name = profile.name
        
    lesson = teacher_agent.generate_custom_lesson(req)
    save_custom_lesson(lesson)
    return lesson

@app.get("/api/recommendations")
async def fetch_recommendations():
    profile = get_profile()
    recs = teacher_agent.get_next_recommendations(profile)
    return {"recommendations": recs}

@app.post("/api/evaluate")
async def evaluate_submission(
    image: UploadFile = File(...),
    lesson_id: str = Form(...)
):
    profile = get_profile()
    
    # Fetch lesson metadata
    lesson = None
    if lesson_id.startswith("custom_"):
        lesson = get_custom_lesson(lesson_id)
    if not lesson:
        lesson = get_lesson_plan(lesson_id)
        
    if not lesson:
        # Fallback dummy lesson plan for grading
        lesson = get_lesson_plan("jk_trace_straight_lines")
        lesson.id = lesson_id
        lesson.title = "Custom Worksheet Practice"

    # Save uploaded image file
    ext = os.path.splitext(image.filename)[1] or ".jpg"
    submission_id = f"sub_{uuid.uuid4().hex[:10]}"
    filename = f"{submission_id}{ext}"
    file_path = os.path.join(UPLOADS_DIR, filename)
    
    image_bytes = await image.read()
    with open(file_path, "wb") as f:
        f.write(image_bytes)
        
    # Evaluate via TeacherAgent
    evaluation = teacher_agent.evaluate_worksheet(
        image_bytes=image_bytes,
        lesson=lesson,
        child_profile=profile,
        submission_id=submission_id
    )
    
    # Save to SQLite and update profile
    record = save_submission(
        submission_id=submission_id,
        child_name=profile.name,
        lesson_id=lesson.id,
        grade=lesson.grade,
        domain=lesson.domain,
        image_filename=filename,
        evaluation=evaluation
    )
    
    return {
        "status": "success",
        "submission": record,
        "evaluation": evaluation
    }

@app.get("/api/portfolio")
async def fetch_portfolio():
    submissions = get_all_submissions()
    return {"submissions": submissions}
