from typing import Dict, Any, List

def analyze_skill_gap(user_skills: List[str], target_skills: List[str]) -> Dict[str, Any]:
    user_set = set([s.lower() for s in user_skills])
    target_set = set([s.lower() for s in target_skills])
    
    strong = list(user_set.intersection(target_set))
    missing = list(target_set - user_set)
    
    return {
        "strong": strong,
        "developing": [],
        "missing": missing,
        "priority": "High" if len(missing) > 2 else "Low",
        "learning_recommendation": f"Focus on learning: {', '.join(missing[:3])}" if missing else "You are well equipped!"
    }
