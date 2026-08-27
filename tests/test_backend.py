import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure app is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.curriculum import CURRICULUM_SKILLS, get_lesson_plan, compute_skills_status
from app.models import GradeLevel

client = TestClient(app)

def test_profile_api():
    response = client.get("/api/profile")
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert data["profile"]["name"] == "Akira"
    assert data["profile"]["grade"] == "JK"

def test_curriculum_api():
    response = client.get("/api/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert len(data["nodes"]) >= 20

def test_lesson_fetch():
    response = client.get("/api/lessons/jk_trace_straight_lines")
    assert response.status_code == 200
    lesson = response.json()
    assert lesson["id"] == "jk_trace_straight_lines"
    assert len(lesson["exercises"]) >= 1

def test_recommendations():
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) >= 1

def test_custom_worksheet_generation():
    req = {
        "grade": "JK",
        "domain": "phonics",
        "topic": "Dinosaurs",
        "child_name": "Maya",
        "custom_prompt": "Letter D and dinosaur footprints"
    }
    response = client.post("/api/lessons/generate", json=req)
    assert response.status_code == 200
    lesson = response.json()
    assert "exercises" in lesson
    assert len(lesson["exercises"]) >= 1
    assert "id" in lesson
    assert lesson["is_custom"] is True

def test_custom_worksheet_all_domains_fallback():
    from app.agent import teacher_agent
    from app.models import CustomGenerateRequest, SkillDomain, GradeLevel
    
    domains = [
        SkillDomain.PHONICS,
        SkillDomain.NUMERACY,
        SkillDomain.TRACING,
        SkillDomain.SHAPES_COLORS,
        SkillDomain.LOGIC_PATTERNS,
        SkillDomain.READING_WRITING
    ]
    for dom in domains:
        req = CustomGenerateRequest(
            grade=GradeLevel.JK,
            domain=dom,
            topic="Space",
            child_name="Akira",
            custom_prompt="Letter S and planets"
        )
        lesson = teacher_agent._generate_fallback_custom_lesson(req, f"custom_test_{dom.value}")
        assert lesson.title
        assert len(lesson.exercises) >= 3
        assert lesson.domain == dom
        assert lesson.is_custom is True

def test_multi_grade_progression():
    # Test that mastering JK prerequisites unlocks SK
    jk_mastered = [s["id"] for s in CURRICULUM_SKILLS if s["grade"] == GradeLevel.JK]
    skills_map = compute_skills_status(jk_mastered, GradeLevel.JK)
    
    # SK starting skill should now be available
    assert skills_map["sk_cvc_short_a"]["status"] == "available"
