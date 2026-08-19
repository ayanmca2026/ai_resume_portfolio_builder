from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Dict, Any
from app.services.document_parser import extract_resume_text
import mimetypes

router = APIRouter()

ALLOWED_MIMES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword"
]
MAX_SIZE = 5 * 1024 * 1024 # 5MB

@router.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX allowed.")
        
    file_bytes = await file.read()
    if len(file_bytes) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")
        
    text = extract_resume_text(file.filename, file_bytes)
    
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from the document.")
        
    return {
        "filename": file.filename,
        "extracted_length": len(text),
        "status": "success",
        "message": "Resume uploaded and parsed successfully."
    }
