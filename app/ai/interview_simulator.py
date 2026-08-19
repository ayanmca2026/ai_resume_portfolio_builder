from typing import Dict, Any, List

def generate_interview_questions(twin: Dict[str, Any], target_role: str) -> List[Dict[str, str]]:
    questions = [
        {"type": "HR", "question": "Tell me about yourself and why you're a good fit for this role."},
        {"type": "Behavioral", "question": "Describe a time you faced a difficult technical challenge."}
    ]
    if twin.get("projects"):
        best_project = twin["projects"][0].get("name", "your recent project")
        questions.append({"type": "Project", "question": f"Walk me through the architecture of {best_project}."})
    
    if twin.get("skills"):
        best_skill = twin["skills"][0]
        questions.append({"type": "Technical", "question": f"How would you optimize a slow database query using {best_skill}?"})
        
    return questions

def evaluate_interview_answer(question: str, answer: str) -> Dict[str, Any]:
    words = len(answer.split())
    if words < 10:
        score = 40
        feedback = "Too short. Use the STAR method (Situation, Task, Action, Result) to provide more detail."
    elif words < 30:
        score = 70
        feedback = "Good start, but could use more technical specificity and clear impact metrics."
    else:
        score = 90
        feedback = "Excellent answer. Clear structure and good use of detail."
        
    return {
        "score": score,
        "feedback": feedback
    }
