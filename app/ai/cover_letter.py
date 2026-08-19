from typing import Dict, Any

def generate_cover_letter(career_twin: Dict[str, Any], company: str, target_role: str, jd: str) -> str:
    # MVP deterministic template logic
    name = career_twin.get("identity", {}).get("target_role", "Applicant")
    skills = career_twin.get("skills", [])
    skill_str = ", ".join(skills[:3]) if skills else "my various skills"
    
    letter = f"Dear Hiring Manager at {company},\n\n"
    letter += f"I am writing to express my strong interest in the {target_role} position. "
    letter += f"With my background in {skill_str}, I am confident in my ability to contribute effectively.\n\n"
    
    if career_twin.get("projects"):
        best_project = career_twin["projects"][0]
        letter += f"In my recent project '{best_project.get('name')}', I tackled '{best_project.get('problem')}'.\n\n"
    
    letter += "I look forward to discussing how my experiences align with your needs.\n\n"
    letter += "Sincerely,\nApplicant"
    return letter
