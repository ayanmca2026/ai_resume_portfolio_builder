import os
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import get_db
from app.database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_e2e_final.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_complete_workflow(client):
    db = TestingSessionLocal()
    from app.models.user import User
    from app.models.profile import Profile
    from app.core.security import get_password_hash
    
    # 1. Register User directly for E2E
    user = User(email="e2e_direct@example.com", hashed_password=get_password_hash("pass"), full_name="E2E User")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 3. Create Profile
    profile = Profile(user_id=user.id, target_role="Python Dev", location="NY")
    db.add(profile)
    db.commit()
    
    # 4. We can directly call the AI functions to verify they don't crash
    from app.ai.career_twin import build_career_twin
    from app.documents.pdf import generate_resume_pdf
    from app.documents.docx_gen import generate_resume_docx
    from app.ai.ats_engine import scan_ats
    from app.ai.skill_analyzer import analyze_skill_gap
    from app.ai.cover_letter import generate_cover_letter
    from app.portfolio.generator import generate_portfolio_html
    from app.ai.career_coach import coach_chat
    from app.ai.command_router import route_command
    from app.ai.job_matcher import match_job
    
    # Career Twin
    twin = build_career_twin(user.id, db)
    assert "Python Dev" in twin["identity"]["target_role"]
    
    # Documents
    pdf_path = generate_resume_pdf({"name": "E2E", "skills": ["Python"]}, "generated/e2e.pdf")
    assert os.path.exists(pdf_path)
    docx_path = generate_resume_docx({"name": "E2E", "skills": ["Python"]}, "generated/e2e.docx")
    assert os.path.exists(docx_path)
    
    # ATS
    ats = scan_ats("Python FastAPI", "Python Docker")
    assert "score" in ats
    
    # Job Match
    match = match_job(twin, "Python")
    assert "overall_match" in match
    
    # Skill Gap
    gap = analyze_skill_gap(["Python"], ["Python", "Docker"])
    assert "docker" in gap["missing"]
    
    # Cover Letter
    cl = generate_cover_letter(twin, "Acme Corp", "Python Dev", "JD")
    assert "Acme Corp" in cl
    
    # Portfolio
    port = generate_portfolio_html(twin)
    assert "<html>" in port
    
    # Coach
    ans = coach_chat(twin, "How are my skills?")
    assert "skills" in ans
    
    # Command Router
    route = route_command("generate resume", twin)
    assert route["action"] == "navigate"
    
    db.close()
