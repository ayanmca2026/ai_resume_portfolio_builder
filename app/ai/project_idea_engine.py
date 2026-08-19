from typing import Dict, Any, List

def generate_project_idea(target_role: str, missing_skills: List[str]) -> Dict[str, Any]:
    skill = missing_skills[0] if missing_skills else "Python"
    return {
        "target_role": target_role,
        "project_name": f"{target_role.split()[0]} {skill} Engine",
        "difficulty": "Advanced",
        "skills": [skill, "FastAPI", "Docker"],
        "career_value": 90,
        "why_it_helps": f"Fills your gap in {skill} while building a realistic product.",
        "roadmap": ["Design API", f"Implement {skill} logic", "Deploy via Docker"]
    }
