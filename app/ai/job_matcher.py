from typing import Dict, Any, List
import re

def match_job(career_twin: Dict[str, Any], job_description: str) -> Dict[str, Any]:
    jd_lower = job_description.lower()
    skills = [s.lower() for s in career_twin.get("skills", [])]
    
    matched_skills = [s for s in skills if s in jd_lower]
    
    match_score = len(matched_skills) / max(len(skills), 1) * 100
    if not skills:
        match_score = 0.0

    return {
        "overall_match": min(int(match_score) + 40, 100), # Boost for MVP
        "matched_skills": matched_skills,
        "missing_skills": ["example_missing_skill_1", "example_missing_skill_2"], # Hardcoded for now without full NLP extraction
        "relevant_projects": [],
        "relevant_experience": [],
        "keyword_gaps": [],
        "recommendations": ["Tailor your resume to include more explicit JD keywords"]
    }
