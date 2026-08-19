import os
from app.documents.pdf import generate_resume_pdf
from app.documents.docx_gen import generate_resume_docx
from app.ai.ats_engine import scan_ats
from app.ai.job_matcher import match_job

def test_pdf_generation():
    data = {
        "name": "John Doe",
        "summary": "Expert software engineer.",
        "skills": ["Python", "FastAPI"],
        "education": [{"degree": "BSc Computer Science", "university": "MIT", "graduation_year": "2020"}],
        "experience": [{"role": "Developer", "company": "Tech Corp", "duration": "2020-2024", "responsibilities": "Wrote code."}]
    }
    path = generate_resume_pdf(data, "generated/test_resume.pdf")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 100 # Verify it's not empty
    os.remove(path)

def test_docx_generation():
    data = {
        "name": "John Doe",
        "summary": "Expert software engineer.",
        "skills": ["Python", "FastAPI"]
    }
    path = generate_resume_docx(data, "generated/test_resume.docx")
    assert os.path.exists(path)
    assert os.path.getsize(path) > 100
    os.remove(path)

def test_ats_scan():
    resume = "I am a software engineer with Python and FastAPI experience."
    jd = "We need a Python developer who knows FastAPI and Docker."
    res = scan_ats(resume, jd)
    assert "score" in res
    assert "python" in res["matched_keywords"]
    assert "docker" in res["missing_keywords"]

def test_job_match():
    twin = {"skills": ["Python", "FastAPI"]}
    jd = "Python engineer needed"
    res = match_job(twin, jd)
    assert "overall_match" in res
    assert "python" in [s.lower() for s in res["matched_skills"]]
