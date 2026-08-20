from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

from app.api.auth import get_current_user_from_cookie
from app.database.database import get_db
from app.ai.ats_engine import scan_ats

router = APIRouter(tags=["ats"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def ats_index(request: Request, current_user = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("ats/index.html", {"request": request, "user": current_user})

@router.post("/scan", response_class=HTMLResponse)
async def ats_scan(
    request: Request,
    job_description: str = Form(...),
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    # Get user's latest resume
    query = text("SELECT content_json FROM resumes WHERE user_id = :user_id ORDER BY id DESC LIMIT 1")
    result = db.execute(query, {"user_id": current_user.id}).fetchone()
    
    if not result:
        return templates.TemplateResponse("ats/index.html", {
            "request": request, 
            "user": current_user, 
            "error": "No resume found. Please build your resume first."
        })
    
    try:
        resume_data = json.loads(result.content_json)
        # Flatten resume data into text
        resume_text_parts = []
        if isinstance(resume_data, dict):
            for k, v in resume_data.items():
                if isinstance(v, list):
                    resume_text_parts.append(f"{k}: " + ", ".join([str(item) for item in v]))
                elif isinstance(v, str):
                    resume_text_parts.append(f"{k}: {v}")
                else:
                    resume_text_parts.append(f"{k}: {json.dumps(v)}")
        else:
            resume_text_parts.append(str(resume_data))
        
        resume_text = "\n".join(resume_text_parts)
    except Exception as e:
        resume_text = result.content_json # fallback

    scan_results = scan_ats(resume_text, job_description)
    
    return templates.TemplateResponse("ats/results.html", {
        "request": request, 
        "user": current_user,
        "results": scan_results
    })
