from typing import Dict, Any

def generate_personal_brand(twin: Dict[str, Any]) -> Dict[str, Any]:
    role = twin.get("identity", {}).get("target_role", "Professional")
    skills = twin.get("skills", [])
    skill_str = ", ".join(skills[:3]) if skills else "modern technologies"
    
    headline = f"{role} | Specialist in {skill_str}"
    elevator_pitch = f"Hi, I'm a {role} focused on building scalable solutions using {skill_str}. I enjoy tackling complex problems and delivering high-impact projects."
    
    return {
        "headline": headline,
        "elevator_pitch": elevator_pitch,
        "github_bio": f"Code, Coffee, and {skill_str}.",
        "linkedin_about": elevator_pitch + " Let's connect and build something great!"
    }
