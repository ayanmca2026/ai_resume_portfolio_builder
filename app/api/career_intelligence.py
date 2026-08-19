from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie as get_current_user
from app.models.user import User
from app.ai.career_twin import build_career_twin
from app.ai.career_score import calculate_career_score
from app.ai.career_roadmap import generate_roadmap
from app.ai.project_idea_engine import generate_project_idea
from app.ai.bullet_optimizer import optimize_bullet
from app.ai.interview_simulator import generate_interview_questions, evaluate_interview_answer
from app.ai.personal_brand import generate_personal_brand

router = APIRouter()

@router.get("/career-score")
def get_career_score(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    twin = build_career_twin(current_user.id, db)
    return calculate_career_score(twin)

@router.get("/roadmap")
def get_roadmap(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    twin = build_career_twin(current_user.id, db)
    target_role = twin.get("identity", {}).get("target_role", "Developer")
    # Simplified missing skills for route
    missing_skills = ["Docker", "Kubernetes"]
    return generate_roadmap(twin, target_role, missing_skills)

@router.get("/project-ideas")
def get_project_ideas(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    twin = build_career_twin(current_user.id, db)
    target_role = twin.get("identity", {}).get("target_role", "Developer")
    return generate_project_idea(target_role, ["Docker"])

@router.post("/optimize-bullet")
def api_optimize_bullet(bullet: str):
    return optimize_bullet(bullet)

@router.get("/personal-brand")
def api_personal_brand(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    twin = build_career_twin(current_user.id, db)
    return generate_personal_brand(twin)

@router.get("/interview/questions")
def api_interview_questions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    twin = build_career_twin(current_user.id, db)
    target_role = twin.get("identity", {}).get("target_role", "Developer")
    return generate_interview_questions(twin, target_role)

@router.post("/interview/evaluate")
def api_evaluate_answer(question: str, answer: str):
    return evaluate_interview_answer(question, answer)
