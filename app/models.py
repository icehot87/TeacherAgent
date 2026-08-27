from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class GradeLevel(str, Enum):
    JK = "JK"          # Junior Kindergarten (Ages 3.5 - 5)
    SK = "SK"          # Senior Kindergarten (Ages 5 - 6)
    GRADE1 = "Grade 1" # Grade 1 (Ages 6 - 7)
    GRADE2 = "Grade 2" # Grade 2 (Ages 7 - 8)

class SkillDomain(str, Enum):
    TRACING = "tracing"          # Fine Motor & Pre-Writing
    PHONICS = "phonics"          # Letters, Sounds, CVC Words
    NUMERACY = "numeracy"        # Counting, Numbers, Addition/Subtraction
    SHAPES_COLORS = "shapes"     # Visual Discrimination & Shapes
    LOGIC_PATTERNS = "logic"     # Patterns, Mazes, Logic
    READING_WRITING = "reading"  # Reading Comprehension & Writing

class ExerciseItem(BaseModel):
    id: str
    type: str # 'trace_line', 'trace_letter', 'trace_number', 'count_items', 'circle_item', 'match_pair', 'fill_pattern', 'math_problem', 'cvc_box', 'reading_qa'
    prompt: str
    data: Dict[str, Any] = Field(default_factory=dict)
    # Example data:
    # trace_letter: {"letter": "A", "words": ["Apple", "Ant"], "case": "upper", "strokes": 3}
    # count_items: {"target_count": 4, "item_icon": "star", "options": [3, 4, 5]}
    # fill_pattern: {"sequence": ["circle", "square", "circle", "square"], "choices": ["circle", "square", "triangle"], "answer": "circle"}
    # math_problem: {"operand1": 3, "operand2": 2, "operator": "+", "answer": 5}
    # cvc_box: {"word": "CAT", "missing_index": 1, "image_hint": "cat"}

class LessonPlan(BaseModel):
    id: str
    grade: GradeLevel
    domain: SkillDomain
    skill_id: str
    title: str
    subtitle: str
    description: str
    difficulty: int = 1 # 1 to 5
    instructions_for_child: str
    instructions_for_parent: str
    exercises: List[ExerciseItem]
    target_objectives: List[str]
    created_at: Optional[str] = None
    is_custom: bool = False

class SkillProgress(BaseModel):
    skill_id: str
    domain: SkillDomain
    grade: GradeLevel
    title: str
    mastery_score: float = 0.0 # 0.0 to 1.0 (1.0 = 100% mastered)
    stars_earned: int = 0
    attempts: int = 0
    status: str = "locked" # "locked", "available", "in_progress", "mastered"
    last_practiced: Optional[str] = None

class ChildProfile(BaseModel):
    name: str = "Akira"
    grade: GradeLevel = GradeLevel.JK
    age: float = 4.0
    avatar: str = "🌟"
    total_stars: int = 0
    worksheets_completed: int = 0
    streak_days: int = 1
    theme_preference: str = "Animals & Space"
    skills_progress: Dict[str, SkillProgress] = Field(default_factory=dict)
    mastered_skills: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class StrokeAnalysisItem(BaseModel):
    item_label: str
    observed: str
    quality: str # "excellent", "good", "needs_practice"
    tip: Optional[str] = None

class EvaluationResult(BaseModel):
    submission_id: str
    lesson_id: str
    lesson_title: str
    grade: GradeLevel
    domain: SkillDomain
    overall_score_percent: int
    stars: int # 1 to 5
    praise_title: str
    praise_message: str
    voice_feedback: str # Friendly script for child audio playback
    strengths: List[str]
    areas_to_practice: List[str]
    detailed_observations: List[StrokeAnalysisItem]
    parent_coaching_tip: str
    recommended_next_lessons: List[Dict[str, Any]]
    promoted_to_next_level: bool = False
    newly_unlocked_skills: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class SubmissionRecord(BaseModel):
    id: str
    child_name: str
    lesson_id: str
    grade: GradeLevel
    domain: SkillDomain
    image_path: str
    evaluation: EvaluationResult
    submitted_at: str

class CustomGenerateRequest(BaseModel):
    grade: GradeLevel = GradeLevel.JK
    domain: SkillDomain = SkillDomain.PHONICS
    topic: str = "Animals"
    target_skill: Optional[str] = None
    child_name: Optional[str] = None
    custom_prompt: Optional[str] = None
