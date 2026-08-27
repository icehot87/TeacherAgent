import os
import json
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models import ChildProfile, GradeLevel, SkillDomain, EvaluationResult, SubmissionRecord, LessonPlan

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
PROFILE_FILE = os.path.join(DATA_DIR, "profile.json")
CUSTOM_LESSONS_FILE = os.path.join(DATA_DIR, "custom_lessons.json")
DB_FILE = os.path.join(DATA_DIR, "teacher_agent.db")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            child_name TEXT,
            lesson_id TEXT,
            grade TEXT,
            domain TEXT,
            image_filename TEXT,
            stars INTEGER,
            score_percent INTEGER,
            praise_title TEXT,
            praise_message TEXT,
            voice_feedback TEXT,
            full_evaluation_json TEXT,
            submitted_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_profile() -> ChildProfile:
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return ChildProfile(**data)
        except Exception as e:
            print(f"Error loading profile: {e}")
    
    # Default initial profile for a JK child
    profile = ChildProfile(
        name="Akira",
        grade=GradeLevel.JK,
        age=4.0,
        avatar="🌟",
        total_stars=0,
        worksheets_completed=0,
        streak_days=1,
        theme_preference="Animals & Space",
        mastered_skills=[],
        skills_progress={}
    )
    save_profile(profile)
    return profile

def save_profile(profile: ChildProfile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile.model_dump(), f, indent=2)

def save_submission(
    submission_id: str,
    child_name: str,
    lesson_id: str,
    grade: GradeLevel,
    domain: SkillDomain,
    image_filename: str,
    evaluation: EvaluationResult
) -> SubmissionRecord:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    submitted_at = datetime.now().isoformat()
    eval_json = json.dumps(evaluation.model_dump())
    
    c.execute("""
        INSERT INTO submissions (
            id, child_name, lesson_id, grade, domain, image_filename,
            stars, score_percent, praise_title, praise_message,
            voice_feedback, full_evaluation_json, submitted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        submission_id,
        child_name,
        lesson_id,
        grade.value,
        domain.value,
        image_filename,
        evaluation.stars,
        evaluation.overall_score_percent,
        evaluation.praise_title,
        evaluation.praise_message,
        evaluation.voice_feedback,
        eval_json,
        submitted_at
    ))
    conn.commit()
    conn.close()
    
    # Update profile stats and mastery
    profile = get_profile()
    profile.total_stars += evaluation.stars
    profile.worksheets_completed += 1
    
    # If 4 or 5 stars, consider this skill mastered or increment mastery
    if evaluation.stars >= 4 and lesson_id not in profile.mastered_skills:
        profile.mastered_skills.append(lesson_id)
        
    save_profile(profile)
    
    return SubmissionRecord(
        id=submission_id,
        child_name=child_name,
        lesson_id=lesson_id,
        grade=grade,
        domain=domain,
        image_path=f"/uploads/{image_filename}",
        evaluation=evaluation,
        submitted_at=submitted_at
    )

def get_all_submissions() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT id, child_name, lesson_id, grade, domain, image_filename,
               stars, score_percent, praise_title, praise_message,
               voice_feedback, full_evaluation_json, submitted_at
        FROM submissions ORDER BY submitted_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    
    submissions = []
    for r in rows:
        eval_data = json.loads(r[11]) if r[11] else {}
        submissions.append({
            "id": r[0],
            "child_name": r[1],
            "lesson_id": r[2],
            "grade": r[3],
            "domain": r[4],
            "image_path": f"/uploads/{r[5]}",
            "stars": r[6],
            "score_percent": r[7],
            "praise_title": r[8],
            "praise_message": r[9],
            "voice_feedback": r[10],
            "evaluation": eval_data,
            "submitted_at": r[12]
        })
    return submissions

def save_custom_lesson(lesson: LessonPlan):
    custom_lessons = load_custom_lessons()
    custom_lessons[lesson.id] = lesson.model_dump()
    with open(CUSTOM_LESSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_lessons, f, indent=2)

def load_custom_lessons() -> Dict[str, Any]:
    if os.path.exists(CUSTOM_LESSONS_FILE):
        try:
            with open(CUSTOM_LESSONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def get_custom_lesson(lesson_id: str) -> Optional[LessonPlan]:
    lessons = load_custom_lessons()
    if lesson_id in lessons:
        return LessonPlan(**lessons[lesson_id])
    return None
