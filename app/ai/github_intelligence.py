from typing import Dict, Any

def analyze_github_repo(repo_url: str) -> Dict[str, Any]:
    # Placeholder for a real GitHub API integration.
    # Deterministic fallback for now.
    repo_name = repo_url.split("/")[-1] if "/" in repo_url else "Repository"
    
    return {
        "name": repo_name,
        "languages": ["Python", "JavaScript"],
        "summary": f"A comprehensive project demonstrating proficiency in Python and JavaScript.",
        "technical_stack": "Python, Node.js",
        "interview_questions": [
            f"What was the most challenging part of building {repo_name}?",
            "How did you structure your repository for maintainability?"
        ]
    }
