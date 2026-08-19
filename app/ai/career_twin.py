from typing import Dict, Any
from app.models.profile import Profile
from app.models.education import Education
from app.models.skill import Skill
from app.models.project import Project
from app.models.experience import Experience
from sqlalchemy.orm import Session

def build_career_twin(user_id: int, db: Session) -> Dict[str, Any]:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    educations = db.query(Education).filter(Education.user_id == user_id).all()
    skills = db.query(Skill).filter(Skill.user_id == user_id).all()
    projects = db.query(Project).filter(Project.user_id == user_id).all()
    experiences = db.query(Experience).filter(Experience.user_id == user_id).all()
    
    twin = {
        "identity": {
            "target_role": profile.target_role if profile else "",
            "summary": profile.professional_summary if profile else ""
        },
        "education": [{"degree": e.degree, "university": e.university, "graduation_year": e.graduation_year} for e in educations],
        "skills": [s.name for s in skills],
        "projects": [{"name": p.name, "problem": p.problem, "technologies": p.technologies} for p in projects],
        "experience": [{"company": e.company, "role": e.role, "duration": e.duration, "responsibilities": e.responsibilities} for e in experiences],
        "career_readiness": 0
    }
    
    # Calculate simple readiness
    score = 0
    if profile: score += 20
    if educations: score += 20
    if skills: score += 20
    if projects: score += 20
    if experiences: score += 20
    twin["career_readiness"] = score
    
    return twin
