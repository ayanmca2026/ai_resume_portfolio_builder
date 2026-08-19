from fastapi import APIRouter, Depends, Request, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie
from app.models.application import JobApplication

router = APIRouter(prefix="/jobs", tags=["jobs"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def list_jobs(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    jobs = db.query(JobApplication).filter(JobApplication.user_id == user.id).all()
    return templates.TemplateResponse("jobs/index.html", {"request": request, "user": user, "jobs": jobs})

@router.get("/new", response_class=HTMLResponse)
async def new_job_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("jobs/new.html", {"request": request, "user": user})

@router.post("/new", response_class=HTMLResponse)
async def create_job(
    request: Request, 
    company: str = Form(...),
    role: str = Form(...),
    location: str = Form(None),
    job_url: str = Form(None),
    job_description: str = Form(None),
    status: str = Form("Saved"),
    notes: str = Form(None),
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_user_from_cookie)
):
    app = JobApplication(
        user_id=user.id,
        company=company,
        role=role,
        location=location,
        job_url=job_url,
        job_description=job_description,
        status=status,
        notes=notes
    )
    db.add(app)
    db.commit()
    return RedirectResponse(url="/jobs", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/{app_id}/delete", response_class=HTMLResponse)
async def delete_job(app_id: int, request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    app = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == user.id).first()
    if app:
        db.delete(app)
        db.commit()
    return RedirectResponse(url="/jobs", status_code=status.HTTP_303_SEE_OTHER)
