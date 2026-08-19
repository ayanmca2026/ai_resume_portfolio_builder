import os
from typing import Dict, Any

def generate_portfolio_html(career_twin: Dict[str, Any], theme: str = "minimal") -> str:
    # A simple deterministic generator outputting static HTML based on the twin
    name = career_twin.get("identity", {}).get("target_role", "Developer Portfolio")
    summary = career_twin.get("identity", {}).get("summary", "Welcome to my portfolio.")
    skills = career_twin.get("skills", [])
    
    html = f"<html><head><title>{name}</title></head><body>"
    html += f"<h1>{name}</h1><p>{summary}</p>"
    
    html += "<h2>Skills</h2><ul>"
    for s in skills:
        html += f"<li>{s}</li>"
    html += "</ul>"
    
    html += "<h2>Projects</h2>"
    for p in career_twin.get("projects", []):
        html += f"<h3>{p.get('name')}</h3><p>{p.get('problem')}</p>"
        
    html += "</body></html>"
    return html
