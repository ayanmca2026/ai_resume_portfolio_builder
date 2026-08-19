import os
import zipfile
from typing import Dict, Any

def generate_application_zip(twin: Dict[str, Any], company: str, role: str, output_path: str) -> str:
    # Generates a ZIP file containing Resume PDF, DOCX, and Cover Letter
    from app.documents.pdf import generate_resume_pdf
    from app.documents.docx_gen import generate_resume_docx
    from app.ai.cover_letter import generate_cover_letter
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf_path = output_path.replace('.zip', '.pdf')
    docx_path = output_path.replace('.zip', '.docx')
    cl_path = output_path.replace('.zip', '_cover_letter.txt')
    
    generate_resume_pdf(twin, pdf_path)
    generate_resume_docx(twin, docx_path)
    cl_text = generate_cover_letter(twin, company, role, "Job Description")
    
    with open(cl_path, "w", encoding="utf-8") as f:
        f.write(cl_text)
        
    with zipfile.ZipFile(output_path, 'w') as zipf:
        zipf.write(pdf_path, arcname="Resume.pdf")
        zipf.write(docx_path, arcname="Resume.docx")
        zipf.write(cl_path, arcname="Cover_Letter.txt")
        
    # Cleanup individual files
    os.remove(pdf_path)
    os.remove(docx_path)
    os.remove(cl_path)
    
    return output_path
