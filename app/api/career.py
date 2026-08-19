from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.auth import get_current_user_from_cookie

from app.ai.career_twin import build_career_twin
from app.ai.career_score import calculate_career_score
from app.ai.career_roadmap import generate_roadmap
from app.ai.skill_analyzer import analyze_skill_gap
from app.ai.career_coach import coach_chat
from app.ai.interview_simulator import generate_interview_questions, evaluate_interview_answer

router = APIRouter(prefix="/career", tags=["career"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def career_dashboard(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    score = calculate_career_score(twin)
    return templates.TemplateResponse("career/index.html", {"request": request, "user": user, "score": score})

@router.get("/roadmap", response_class=HTMLResponse)
async def roadmap_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    roadmap = generate_roadmap(twin)
    return templates.TemplateResponse("career/roadmap.html", {"request": request, "user": user, "roadmap": roadmap})

@router.get("/skills", response_class=HTMLResponse)
async def skills_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    target_skills = ['Python', 'JavaScript', 'Docker', 'SQL', 'Git', 'AWS', 'React', 'TypeScript']
    gap = analyze_skill_gap(twin, target_skills)
    return templates.TemplateResponse("career/skills.html", {"request": request, "user": user, "gap": gap})

@router.get("/coach", response_class=HTMLResponse)
async def coach_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("career/coach.html", {"request": request, "user": user})

@router.post("/coach", response_class=HTMLResponse)
async def coach_chat_endpoint(request: Request, message: str = Form(...), db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    response = coach_chat(twin, message)
    return templates.TemplateResponse("career/coach.html", {"request": request, "user": user, "question": message, "answer": response})

@router.get("/interview", response_class=HTMLResponse)
async def interview_page(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    questions = generate_interview_questions(twin, "Software Engineer")
    return templates.TemplateResponse("career/interview.html", {"request": request, "user": user, "questions": questions})

@router.post("/interview/evaluate", response_class=HTMLResponse)
async def evaluate_interview(request: Request, question: str = Form(...), answer: str = Form(...), db: Session = Depends(get_db), user: dict = Depends(get_current_user_from_cookie)):
    twin = build_career_twin(user)
    result = evaluate_interview_answer(twin, question, answer)
    return templates.TemplateResponse("career/interview_result.html", {"request": request, "user": user, "question": question, "answer": answer, "evaluation": result})
