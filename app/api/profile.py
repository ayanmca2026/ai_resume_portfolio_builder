from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie
from app.models.user import User
from app.models.profile import Profile
from app.ai.career_twin import build_career_twin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse, name="profile")
async def view_profile(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    return templates.TemplateResponse(request, "profile/index.html", {"request": request, "user": current_user, "profile": profile})

@router.post("/", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    phone: str = Form(None),
    location: str = Form(None),
    linkedin_url: str = Form(None),
    github_url: str = Form(None),
    portfolio_url: str = Form(None),
    target_role: str = Form(None),
    professional_summary: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        
    profile.phone = phone
    profile.location = location
    profile.linkedin_url = linkedin_url
    profile.github_url = github_url
    profile.portfolio_url = portfolio_url
    profile.target_role = target_role
    profile.professional_summary = professional_summary
    
    db.commit()
    
    # Force twin update
    build_career_twin(current_user.id, db)
    
    return RedirectResponse(url="/dashboard", status_code=303)
