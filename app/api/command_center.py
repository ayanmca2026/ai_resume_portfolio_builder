from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie

from app.ai.career_twin import build_career_twin
from app.ai.command_router import route_command

router = APIRouter(prefix="/command-center", tags=["command_center"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def command_center_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("command_center/index.html", {"request": request, "user": user})

@router.post("/", response_class=HTMLResponse)
async def command_center_post(request: Request, command: str = Form(...), db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    result = route_command(twin, command)
    return templates.TemplateResponse("command_center/index.html", {"request": request, "user": user, "command": command, "result": result})
