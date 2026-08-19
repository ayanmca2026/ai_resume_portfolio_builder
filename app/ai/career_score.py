from typing import Dict, Any

def calculate_career_score(twin: Dict[str, Any]) -> Dict[str, Any]:
    # Base deterministic scoring from twin
    skills = len(twin.get("skills", []))
    projs = len(twin.get("projects", []))
    exps = len(twin.get("experience", []))
    
    skill_score = min(skills * 10, 100)
    proj_score = min(projs * 20, 100)
    exp_score = min(exps * 15, 100)
    
    overall = (skill_score + proj_score + exp_score) // 3
    if overall == 0:
        overall = 10
        
    improvements = []
    if projs < 2:
        improvements.append("Add more detailed project outcomes.")
    if skills < 5:
        improvements.append("Add more technical skills to your profile.")
    if not improvements:
        improvements.append("Tailor your resume for specific target roles.")
        
    return {
        "overall": overall,
        "resume": min(overall + 5, 100),
        "skills": skill_score,
        "projects": proj_score,
        "experience": exp_score,
        "improvements": improvements
    }
