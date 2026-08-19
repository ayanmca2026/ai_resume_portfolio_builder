import os
import io
import fitz  # PyMuPDF
from docx import Document
from typing import Optional

def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        doc = fitz.open("pdf", file_bytes)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""

def extract_docx_text(file_bytes: bytes) -> str:
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ""

def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    ext = filename.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_pdf_text(file_bytes)
    elif ext in ['doc', 'docx']:
        return extract_docx_text(file_bytes)
    return ""
