from typing import Dict, Any

def route_command(command_text: str, career_twin: Dict[str, Any]) -> Dict[str, Any]:
    cmd = command_text.lower()
    
    if "resume" in cmd:
        return {"action": "navigate", "target": "/resume", "message": "Redirecting to Resume Studio..."}
    elif "portfolio" in cmd:
        return {"action": "generate_portfolio", "message": "Generating your portfolio..."}
    elif "skill" in cmd:
        return {"action": "analyze_skills", "message": "Analyzing your skill gaps..."}
    else:
        return {"action": "chat", "message": "I can help you build your resume, portfolio, or analyze your skills."}
