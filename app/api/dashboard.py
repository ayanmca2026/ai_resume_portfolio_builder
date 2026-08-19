from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.api.auth import get_current_user_from_cookie
from app.models.user import User
from app.models.profile import Profile
from app.models.education import Education
from app.models.skill import Skill
from app.models.project import Project
from app.models.experience import Experience
from app.models.certification import Certification
from app.models.achievement import Achievement
from app.models.resume import Resume
from app.models.application import JobApplication
from app.database.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def calculate_profile_strength(db: Session, user_id: int) -> int:
    score = 0
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        score += 20
        if profile.professional_summary:
            score += 5
        if profile.target_role:
            score += 5
    if db.query(Education).filter(Education.user_id == user_id).count() > 0:
        score += 15
    skill_count = db.query(Skill).filter(Skill.user_id == user_id).count()
    if skill_count > 0:
        score += min(skill_count * 4, 20)
    project_count = db.query(Project).filter(Project.user_id == user_id).count()
    if project_count > 0:
        score += min(project_count * 5, 15)
    if db.query(Experience).filter(Experience.user_id == user_id).count() > 0:
        score += 10
    if db.query(Certification).filter(Certification.user_id == user_id).count() > 0:
        score += 5
    if db.query(Achievement).filter(Achievement.user_id == user_id).count() > 0:
        score += 5
    return min(score, 100)

def calculate_career_readiness(db: Session, user_id: int) -> int:
    score = 0
    if db.query(Profile).filter(Profile.user_id == user_id).first():
        score += 15
    if db.query(Education).filter(Education.user_id == user_id).count() > 0:
        score += 15
    if db.query(Skill).filter(Skill.user_id == user_id).count() >= 3:
        score += 20
    if db.query(Project).filter(Project.user_id == user_id).count() >= 2:
        score += 20
    if db.query(Experience).filter(Experience.user_id == user_id).count() > 0:
        score += 15
    if db.query(Resume).filter(Resume.user_id == user_id).count() > 0:
        score += 15
    return min(score, 100)

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    profile_strength = calculate_profile_strength(db, current_user.id)
    career_readiness = calculate_career_readiness(db, current_user.id)
    
    latest_resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
    resume_score = int(latest_resume.ats_score) if latest_resume and latest_resume.ats_score else None
    
    project_count = db.query(Project).filter(Project.user_id == current_user.id).count()
    skill_count = db.query(Skill).filter(Skill.user_id == current_user.id).count()
    app_count = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).count()
    
    return templates.TemplateResponse(request, "dashboard/index.html", {
        "request": request,
        "user": current_user,
        "profile_strength": profile_strength,
        "career_readiness": career_readiness,
        "resume_score": resume_score,
        "project_count": project_count,
        "skill_count": skill_count,
        "app_count": app_count,
    })
