from typing import Dict, Any

def optimize_bullet(bullet: str) -> Dict[str, Any]:
    length = len(bullet.split())
    if length < 5:
        score = "Weak"
        improved = f"Developed and optimized a {bullet.lower()} solution, resulting in improved performance."
    elif length < 10:
        score = "Good"
        improved = bullet + " ensuring high reliability."
    else:
        score = "Excellent"
        improved = bullet
        
    return {
        "score": score,
        "original": bullet,
        "improved": improved
    }
