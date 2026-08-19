import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import get_db
from app.database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_phase5.db"

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

def test_phase5_engines():
    from app.ai.career_score import calculate_career_score
    from app.ai.career_roadmap import generate_roadmap
    from app.ai.project_idea_engine import generate_project_idea
    from app.ai.bullet_optimizer import optimize_bullet
    from app.ai.application_pack import generate_application_zip
    import os
    
    twin = {
        "identity": {"target_role": "AI Engineer"},
        "skills": ["Python", "Machine Learning"],
        "projects": [{"name": "AI App", "technologies": "Python"}]
    }
    
    score = calculate_career_score(twin)
    assert score["overall"] > 0
    
    roadmap = generate_roadmap(twin, "AI Engineer", ["Docker"])
    assert "30_days" in roadmap
    
    proj = generate_project_idea("AI Engineer", ["Docker"])
    assert "Docker" in proj["skills"]
    
    opt = optimize_bullet("Did some coding.")
    assert "score" in opt
    
    zip_path = "generated/test_app_pack.zip"
    generate_application_zip(twin, "Google", "AI Engineer", zip_path)
    assert os.path.exists(zip_path)
    os.remove(zip_path)

def test_intelligence_routes(client):
    db = TestingSessionLocal()
    from app.models.user import User
    from app.core.security import get_password_hash
    from app.core.security import create_access_token
    import datetime
    
    # Setup test user
    user = User(email="p5@example.com", hashed_password=get_password_hash("pass"), full_name="P5 User")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=datetime.timedelta(minutes=30))
    client.cookies.set("access_token", f"Bearer {access_token}")
    
    r_score = client.get("/intelligence/career-score")
    assert r_score.status_code == 200
    
    r_brand = client.get("/intelligence/personal-brand")
    assert r_brand.status_code == 200
    
    r_q = client.get("/intelligence/interview/questions")
    assert r_q.status_code == 200
    
    db.close()
