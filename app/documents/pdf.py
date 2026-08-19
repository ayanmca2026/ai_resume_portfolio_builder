import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_resume_pdf(resume_data: dict, output_path: str) -> str:
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=12,
        textColor=colors.HexColor("#2C3E50")
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        textColor=colors.HexColor("#34495E"),
        borderPadding=0,
        borderWidth=0,
        borderColor=colors.white
    )
    normal_style = styles['Normal']
    
    story = []
    
    # Name
    story.append(Paragraph(resume_data.get("name", "User Name"), title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    if resume_data.get("summary"):
        story.append(Paragraph("Professional Summary", heading_style))
        story.append(Paragraph(resume_data["summary"], normal_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Skills
    if resume_data.get("skills"):
        story.append(Paragraph("Skills", heading_style))
        skills_str = ", ".join(resume_data["skills"])
        story.append(Paragraph(skills_str, normal_style))
        story.append(Spacer(1, 0.2*inch))
        
    # Experience
    if resume_data.get("experience"):
        story.append(Paragraph("Experience", heading_style))
        for exp in resume_data["experience"]:
            exp_text = f"<b>{exp.get('role', '')}</b> at {exp.get('company', '')} ({exp.get('duration', '')})"
            story.append(Paragraph(exp_text, normal_style))
            if exp.get('responsibilities'):
                story.append(Paragraph(exp.get('responsibilities'), normal_style))
            story.append(Spacer(1, 0.1*inch))
            
    # Education
    if resume_data.get("education"):
        story.append(Paragraph("Education", heading_style))
        for edu in resume_data["education"]:
            edu_text = f"<b>{edu.get('degree', '')}</b>, {edu.get('university', '')} ({edu.get('graduation_year', '')})"
            story.append(Paragraph(edu_text, normal_style))
            story.append(Spacer(1, 0.1*inch))
            
    doc.build(story)
    return output_path
