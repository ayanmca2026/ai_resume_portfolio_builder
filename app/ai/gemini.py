from app.ai.base import AIProvider
from typing import Dict, Any, List
import json
import logging
import google.generativeai as genai
from google.generativeai.types import generation_types

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
            self._is_active = True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self._is_active = False
            
    def _safe_generate(self, prompt: str, fallback: Any) -> Any:
        if not self._is_active:
            logger.warning("Gemini is inactive, returning fallback.")
            return fallback
        try:
            response = self.model.generate_content(prompt)
            if response.text:
                # Try to extract JSON if it was requested
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text[7:-3]
                return text
            return fallback
        except generation_types.StopCandidateException:
            logger.warning("Gemini generation stopped unexpectedly.")
            return fallback
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return fallback
            
    def _parse_json_or_fallback(self, response_text: str, fallback: Any) -> Any:
        if isinstance(response_text, str):
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                logger.error("Failed to parse Gemini JSON output")
                return fallback
        return fallback

    def generate_resume(self, profile_data: Dict[str, Any], target_role: str) -> Dict[str, Any]:
        fallback = {
            "summary": f"Fallback: Highly motivated professional seeking {target_role} role.",
            "skills": profile_data.get("skills", []),
            "experience": profile_data.get("experience", []),
            "education": profile_data.get("education", [])
        }
        prompt = f"Generate a JSON resume for {target_role} using this profile data: {json.dumps(profile_data)}. Return ONLY valid JSON with keys: 'summary', 'skills', 'experience', 'education'."
        response_text = self._safe_generate(prompt, fallback=json.dumps(fallback))
        return self._parse_json_or_fallback(response_text, fallback)
        
    def scan_ats(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        fallback = {
            "score": 50,
            "keyword_score": 50,
            "matched_keywords": [],
            "missing_keywords": ["fallback_missing"],
            "recommendations": ["AI service temporarily unavailable, using fallback."],
            "warnings": []
        }
        prompt = f"Act as an ATS. Compare this resume:\n{resume_text}\n\nWith this job description:\n{job_description}\n\nReturn ONLY valid JSON with keys: 'score' (0-100), 'keyword_score', 'matched_keywords' (list), 'missing_keywords' (list), 'recommendations' (list), 'warnings' (list)."
        response_text = self._safe_generate(prompt, fallback=json.dumps(fallback))
        return self._parse_json_or_fallback(response_text, fallback)
        
    def analyze_skill_gap(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        fallback = {
            "strong": user_skills,
            "missing": ["React", "Kubernetes"],
            "recommendations": ["Build a small fullstack app"]
        }
        prompt = f"Analyze skill gap for target role {target_role} given user skills {user_skills}. Return ONLY valid JSON with keys 'strong' (list), 'missing' (list), 'recommendations' (list)."
        response_text = self._safe_generate(prompt, fallback=json.dumps(fallback))
        return self._parse_json_or_fallback(response_text, fallback)

    def career_coach_chat(self, history: List[Dict[str, str]], message: str) -> str:
        fallback = "[Gemini Fallback] I advise you to focus on tailoring your resume."
        prompt = f"You are an AI Career Coach. The user says: {message}\nReply concisely and professionally."
        response_text = self._safe_generate(prompt, fallback=fallback)
        return str(response_text)
