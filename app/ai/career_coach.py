from typing import Dict, Any, List

def coach_chat(career_twin: Dict[str, Any], message: str) -> str:
    if "project" in message.lower() and career_twin.get("projects"):
        return f"Your project '{career_twin['projects'][0]['name']}' is a great talking point for interviews."
    elif "skill" in message.lower():
        return f"You currently have strong skills in: {', '.join(career_twin.get('skills', []))}."
    else:
        return "As your Career Coach, I recommend tailoring your resume to specific job descriptions."
