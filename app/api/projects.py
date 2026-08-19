from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie
from app.models.user import User
from app.models.project import Project
from app.ai.career_twin import build_career_twin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse, name="projects")
async def list_projects(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_cookie)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return templates.TemplateResponse(request, "projects/index.html", {"request": request, "user": current_user, "projects": projects})

@router.get("/new", response_class=HTMLResponse, name="new_project")
async def new_project_page(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "projects/new.html", {"request": request, "user": current_user})

@router.post("/new", response_class=HTMLResponse)
async def create_project(
    request: Request,
    name: str = Form(...),
    problem: str = Form(None),
    solution: str = Form(None),
    technologies: str = Form(None),
    github_url: str = Form(None),
    live_url: str = Form(None),
    role: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_cookie)
):
    project = Project(
        user_id=current_user.id,
        name=name,
        problem=problem,
        solution=solution,
        technologies=technologies,
        github_url=github_url,
        live_url=live_url,
        contribution=role
    )
    db.add(project)
    db.commit()
    
    build_career_twin(current_user.id, db)
    
    return RedirectResponse(url="/projects", status_code=303)
