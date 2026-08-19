from typing import Dict, Any

def generate_linkedin_post(twin: Dict[str, Any], topic: str, tone: str) -> str:
    # Deterministic generation
    post = f"Excited to share some updates!\n\n"
    if topic == "Project Announcement" and twin.get("projects"):
        p = twin["projects"][0]
        post += f"I just wrapped up {p.get('name')}. It was an incredible journey solving '{p.get('problem')}'.\n"
        post += f"Tech stack: {p.get('technologies')}\n\n"
    else:
        post += f"I've been diving deep into new learning areas and applying them to my workflows.\n\n"
        
    if tone == "Professional":
        post += "Looking forward to bringing this expertise to my next role. #CareerGrowth #Learning"
    else:
        post += "Building in public is fun! Let me know what you think. #BuildInPublic #Tech"
        
    return post
