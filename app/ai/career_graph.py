from typing import Dict, Any, List

def build_career_graph(twin: Dict[str, Any]) -> Dict[str, Any]:
    skills = twin.get("skills", [])
    projects = twin.get("projects", [])
    
    # Simple deterministic linkage between skills and projects
    graph = {
        "nodes": [{"id": s, "type": "skill", "label": s} for s in skills],
        "edges": []
    }
    
    for p in projects:
        p_name = p.get("name")
        graph["nodes"].append({"id": p_name, "type": "project", "label": p_name})
        p_tech = p.get("technologies", "").split(",")
        for t in p_tech:
            t_clean = t.strip()
            if t_clean in skills:
                graph["edges"].append({"source": t_clean, "target": p_name, "type": "used_in"})
                
    return graph
