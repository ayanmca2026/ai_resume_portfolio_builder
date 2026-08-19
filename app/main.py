from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.database.database import engine
from app.database.base import Base
# Routers
from app.api import auth, dashboard, upload, onboarding, projects
from app.api import resume, ats, cover_letter, portfolio, career, jobs, command_center
from app.api.career_intelligence import router as intel_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Auth
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# Core pages
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
# Resume & Documents
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(upload.router, tags=["upload"])
# AI Tools
app.include_router(ats.router, prefix="/ats", tags=["ats"])
app.include_router(cover_letter.router, prefix="/cover-letter", tags=["cover-letter"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(career.router, prefix="/career", tags=["career"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(command_center.router, prefix="/command-center", tags=["command-center"])
# Intelligence API
app.include_router(intel_router, prefix="/intelligence", tags=["intelligence"])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request, "landing.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "ai_provider": settings.AI_PROVIDER}

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(request, "errors/404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return templates.TemplateResponse(request, "errors/500.html", {"request": request}, status_code=500)
