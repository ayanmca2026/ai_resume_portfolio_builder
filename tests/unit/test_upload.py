import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_invalid_mime():
    response = client.post(
        "/upload/resume",
        files={"file": ("test.txt", b"Hello", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_upload_valid_pdf_empty():
    response = client.post(
        "/upload/resume",
        files={"file": ("test.pdf", b"%PDF-1.4 empty", "application/pdf")}
    )
    assert response.status_code == 400
    assert "Could not extract text" in response.json()["detail"]
