import json
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.auth import get_current_user_from_cookie
from app.database.database import get_db
from app.core.config import settings
from app.ai.career_twin import build_career_twin
from app.documents.pdf import generate_resume_pdf
from app.documents.docx_gen import generate_resume_docx
from app.models.resume import Resume

router = APIRouter(tags=["resume"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def list_resumes(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    resumes = db.query(Resume).filter(Resume.user_id == user.id).all()
    return templates.TemplateResponse("resume/index.html", {"request": request, "resumes": resumes, "user": user})

@router.get("/build", response_class=HTMLResponse)
def build_resume_form(request: Request):
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("resume/build.html", {"request": request, "user": user})

@router.post("/build")
def build_resume_post(
    request: Request,
    target_role: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
        
    career_twin_data = build_career_twin(user.id)
    resume_data = {
        "target_role": target_role,
        "identity": career_twin_data.get("identity"),
        "education": career_twin_data.get("education"),
        "skills": career_twin_data.get("skills"),
        "projects": career_twin_data.get("projects"),
        "experience": career_twin_data.get("experience")
    }
    
    new_resume = Resume(
        user_id=user.id,
        target_role=target_role,
        content_json=json.dumps(resume_data),
        template_name="default",
        ats_score=0
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    pdf_path = str(settings.GENERATED_DIR / f'resume_{user.id}_{new_resume.id}.pdf')
    docx_path = str(settings.GENERATED_DIR / f'resume_{user.id}_{new_resume.id}.docx')
    
    generate_resume_pdf(resume_data, pdf_path)
    generate_resume_docx(resume_data, docx_path)
    
    new_resume.pdf_path = pdf_path
    new_resume.docx_path = docx_path
    db.commit()
    
    return RedirectResponse(url="/resume", status_code=303)

@router.get("/{resume_id}/download/pdf")
def download_pdf(request: Request, resume_id: int, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
        
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume or not resume.pdf_path:
        raise HTTPException(status_code=404, detail="Resume PDF not found")
        
    return FileResponse(path=resume.pdf_path, filename=f"resume_{resume_id}.pdf", media_type='application/pdf')

@router.get("/{resume_id}/download/docx")
def download_docx(request: Request, resume_id: int, db: Session = Depends(get_db)):
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
        
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume or not resume.docx_path:
        raise HTTPException(status_code=404, detail="Resume DOCX not found")
        
    return FileResponse(path=resume.docx_path, filename=f"resume_{resume_id}.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
