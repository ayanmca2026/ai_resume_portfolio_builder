from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AIProvider(ABC):
    
    @abstractmethod
    def generate_resume(self, profile_data: Dict[str, Any], target_role: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def scan_ats(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def analyze_skill_gap(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def career_coach_chat(self, history: List[Dict[str, str]], message: str) -> str:
        pass
