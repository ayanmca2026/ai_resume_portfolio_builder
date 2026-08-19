from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.auth import get_current_user_from_cookie
from app.database.database import get_db
from app.ai.career_twin import build_career_twin
from app.portfolio.generator import generate_portfolio_html

router = APIRouter(prefix="/portfolio", tags=["portfolio"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def portfolio_index(
    request: Request, 
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    career_twin = build_career_twin(current_user.id, db)
    # Default theme could be passed or hardcoded
    portfolio_html = generate_portfolio_html(career_twin, theme="dark")
    
    return templates.TemplateResponse("portfolio/index.html", {
        "request": request, 
        "user": current_user,
        "portfolio_html": portfolio_html
    })
