from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie
from app.models import Profile, Education, Skill, Experience, Certification, Achievement, Project

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_onboarding(
    request: Request,
    user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    educations = db.query(Education).filter(Education.user_id == user.id).all()
    skills = db.query(Skill).filter(Skill.user_id == user.id).all()
    experiences = db.query(Experience).filter(Experience.user_id == user.id).all()
    certifications = db.query(Certification).filter(Certification.user_id == user.id).all()
    achievements = db.query(Achievement).filter(Achievement.user_id == user.id).all()
    
    return templates.TemplateResponse(
        "profile/index.html",
        {
            "request": request,
            "user": user,
            "profile": profile,
            "educations": educations,
            "skills": skills,
            "experiences": experiences,
            "certifications": certifications,
            "achievements": achievements
        }
    )

@router.post("/")
async def post_onboarding(
    request: Request,
    user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
    form = await request.form()
    
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        profile = Profile(user_id=user.id)
        db.add(profile)
        
    profile.phone = form.get("phone", "")
    profile.location = form.get("location", "")
    profile.linkedin_url = form.get("linkedin_url", "")
    profile.github_url = form.get("github_url", "")
    profile.portfolio_url = form.get("portfolio_url", "")
    profile.target_role = form.get("target_role", "")
    profile.industry = form.get("industry", "")
    profile.experience_level = form.get("experience_level", "")
    profile.professional_summary = form.get("professional_summary", "")
    
    # Delete existing lists
    db.query(Education).filter(Education.user_id == user.id).delete()
    db.query(Skill).filter(Skill.user_id == user.id).delete()
    db.query(Experience).filter(Experience.user_id == user.id).delete()
    db.query(Certification).filter(Certification.user_id == user.id).delete()
    db.query(Achievement).filter(Achievement.user_id == user.id).delete()
    
    # Process Education
    edu_degrees = form.getlist("edu_degree[]")
    edu_universities = form.getlist("edu_university[]")
    edu_departments = form.getlist("edu_department[]")
    edu_cgpas = form.getlist("edu_cgpa[]")
    edu_grad_years = form.getlist("edu_graduation_year[]")
    
    for i in range(len(edu_degrees)):
        if edu_degrees[i].strip():
            db.add(Education(
                user_id=user.id,
                degree=edu_degrees[i],
                university=edu_universities[i] if i < len(edu_universities) else "",
                department=edu_departments[i] if i < len(edu_departments) else "",
                cgpa=edu_cgpas[i] if i < len(edu_cgpas) else "",
                graduation_year=edu_grad_years[i] if i < len(edu_grad_years) else ""
            ))
            
    # Process Skills
    skill_names = form.getlist("skill_name[]")
    skill_categories = form.getlist("skill_category[]")
    for i in range(len(skill_names)):
        if skill_names[i].strip():
            db.add(Skill(
                user_id=user.id,
                name=skill_names[i],
                category=skill_categories[i] if i < len(skill_categories) else ""
            ))
            
    # Process Experience
    exp_companies = form.getlist("exp_company[]")
    exp_roles = form.getlist("exp_role[]")
    exp_durations = form.getlist("exp_duration[]")
    exp_responsibilities = form.getlist("exp_responsibilities[]")
    for i in range(len(exp_companies)):
        if exp_companies[i].strip():
            db.add(Experience(
                user_id=user.id,
                company=exp_companies[i],
                role=exp_roles[i] if i < len(exp_roles) else "",
                duration=exp_durations[i] if i < len(exp_durations) else "",
                responsibilities=exp_responsibilities[i] if i < len(exp_responsibilities) else ""
            ))
            
    # Process Certifications
    cert_names = form.getlist("cert_name[]")
    cert_issuers = form.getlist("cert_issuer[]")
    cert_years = form.getlist("cert_year[]")
    cert_urls = form.getlist("cert_url[]")
    for i in range(len(cert_names)):
        if cert_names[i].strip():
            db.add(Certification(
                user_id=user.id,
                name=cert_names[i],
                issuer=cert_issuers[i] if i < len(cert_issuers) else "",
                year=cert_years[i] if i < len(cert_years) else "",
                url=cert_urls[i] if i < len(cert_urls) else ""
            ))
            
    # Process Achievements
    ach_titles = form.getlist("ach_title[]")
    ach_descriptions = form.getlist("ach_description[]")
    ach_years = form.getlist("ach_year[]")
    for i in range(len(ach_titles)):
        if ach_titles[i].strip():
            db.add(Achievement(
                user_id=user.id,
                title=ach_titles[i],
                description=ach_descriptions[i] if i < len(ach_descriptions) else "",
                year=ach_years[i] if i < len(ach_years) else ""
            ))

    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
