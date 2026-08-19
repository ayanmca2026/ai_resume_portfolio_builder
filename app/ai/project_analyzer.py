from typing import Dict, Any

def analyze_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
    tech = project_data.get("technologies", "").split(",")
    complexity = min(len(tech) * 10, 100)
    
    return {
        "technical_complexity": complexity,
        "innovation": 75,
        "resume_value": "High",
        "resume_description": f"Developed a solution using {', '.join(tech)}.",
        "interview_explanation": "Focus on the technical challenges overcome during development."
    }
