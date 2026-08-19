from app.ai.base import AIProvider
from typing import Dict, Any, List

class MockProvider(AIProvider):
    
    def generate_resume(self, profile_data: Dict[str, Any], target_role: str) -> Dict[str, Any]:
        return {
            "summary": f"Experienced professional aiming for {target_role}.",
            "skills": profile_data.get("skills", []),
            "experience": profile_data.get("experience", []),
            "education": profile_data.get("education", [])
        }
        
    def scan_ats(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        return {
            "score": 85,
            "matched_keywords": ["python", "api"],
            "missing_keywords": ["docker"],
            "recommendations": ["Add docker to your skills"]
        }
        
    def analyze_skill_gap(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        return {
            "strong": ["python"],
            "missing": ["docker", "kubernetes"],
            "recommendations": ["Learn docker for deployment"]
        }

    def career_coach_chat(self, history: List[Dict[str, str]], message: str) -> str:
        return f"Mock answer to: {message}"
