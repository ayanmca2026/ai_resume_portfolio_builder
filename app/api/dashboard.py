from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.auth import get_current_user_from_cookie
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse(request, "dashboard/index.html", {"request": request, "user": current_user})
