from typing import Dict, Any, List

def generate_roadmap(twin: Dict[str, Any], target_role: str, missing_skills: List[str]) -> Dict[str, Any]:
    # Use deterministic logic to construct a 30, 60, 90 day roadmap
    top_skill = missing_skills[0] if missing_skills else "advanced architecture"
    second_skill = missing_skills[1] if len(missing_skills) > 1 else "cloud deployment"
    
    roadmap = {
        "30_days": {
            "focus": f"Learn core concepts of {top_skill}",
            "tasks": [
                f"Complete foundational tutorial on {top_skill}",
                "Update GitHub profile",
                "Start a small side project"
            ]
        },
        "60_days": {
            "focus": f"Apply {top_skill} and learn {second_skill}",
            "tasks": [
                f"Integrate {top_skill} into your current portfolio project",
                f"Begin learning {second_skill} fundamentals",
                "Update resume with new learning"
            ]
        },
        "90_days": {
            "focus": "Interview preparation and job application",
            "tasks": [
                "Practice technical interviews",
                f"Deploy project using {second_skill}",
                f"Apply for 5 {target_role} roles"
            ]
        }
    }
    return roadmap
