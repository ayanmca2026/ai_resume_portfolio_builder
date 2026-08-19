from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.database.database import engine
from app.database.base import Base
# Routers
from app.api import auth, dashboard, upload, onboarding, projects
from app.api.career_intelligence import router as intel_router

# Create tables for now (until migrations are fully run)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(upload.router, tags=["upload"])
app.include_router(intel_router, prefix="/intelligence", tags=["intelligence"])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request, "landing.html", {"request": request})

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_provider": settings.AI_PROVIDER
    }
