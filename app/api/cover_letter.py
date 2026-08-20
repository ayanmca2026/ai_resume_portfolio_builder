from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.auth import get_current_user_from_cookie
from app.database.database import get_db
from app.ai.cover_letter import generate_cover_letter
from app.ai.career_twin import build_career_twin

router = APIRouter(tags=["cover_letter"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def cover_letter_index(request: Request, current_user = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("cover_letter/index.html", {"request": request, "user": current_user})

@router.post("/generate", response_class=HTMLResponse)
async def cover_letter_generate(
    request: Request,
    company: str = Form(...),
    target_role: str = Form(...),
    job_description: str = Form(...),
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    career_twin = build_career_twin(current_user.id, db)
    cover_letter_text = generate_cover_letter(career_twin, company, target_role, job_description)
    
    return templates.TemplateResponse("cover_letter/result.html", {
        "request": request, 
        "user": current_user,
        "cover_letter": cover_letter_text,
        "company": company,
        "role": target_role
    })
