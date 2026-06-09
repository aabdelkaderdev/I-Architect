from typing import Dict, Any
import os
from sa.state.schemas import SAState
from sa.utils.llm import evaluate_with_llm

def node_functional(state: SAState) -> Dict[str, Any]:
    req_data = state.get("requirements_data", {})
    functional_reqs = req_data.get("non_asr", [])
    total_functional = len(functional_reqs)
    
    traceability_matrix = state.get("traceability_matrix", {})
    
    # 1. Deterministic mapping coverage
    mapped_functional = sum(1 for req in functional_reqs if req in traceability_matrix and traceability_matrix[req])
    
    if total_functional > 0:
        coverage_score = (mapped_functional / total_functional) * 15.0
    else:
        coverage_score = 0.0
        
    # 2. Deterministic orphan penalty
    orphans = [req for req in functional_reqs if req not in traceability_matrix or not traceability_matrix[req]]
    penalty_points = min(len(orphans), 10) * -1.0
    
    penalties_applied = []
    if penalty_points < 0:
        penalties_applied.append({
            "reason": f"{len(orphans)} functional requirements are orphaned",
            "points": penalty_points,
            "requirement_id": None
        })
        
    # 3. Depth distribution summary
    level_counts = {"system": 0, "container": 0, "component": 0, "unknown": 0}
    total_mapped = 0
    requirements_mapping_details = []
    
    for req in functional_reqs:
        if req in traceability_matrix and traceability_matrix[req]:
            # Get deepest level
            deepest = "unknown"
            for entry in traceability_matrix[req]:
                if entry.get("deepest_level"):
                    deepest = entry["deepest_level"]
                    break
            if deepest in level_counts:
                level_counts[deepest] += 1
            else:
                level_counts["unknown"] += 1
            total_mapped += 1
            requirements_mapping_details.append(f"- {req}: {deepest}")
            
    if total_mapped > 0:
        depth_dist = "\n".join([f"- {lvl}: {count/total_mapped*100:.1f}%" for lvl, count in level_counts.items() if count > 0])
    else:
        depth_dist = "No functional requirements mapped."
        
    requirements_mapping_str = "\n".join(requirements_mapping_details) if requirements_mapping_details else "None"
    
    # 4. LLM call
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "functional_depth.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    else:
        prompt_template = "Context: {depth_distribution}\nMappings: {requirements_mapping}"
        
    prompt_text = prompt_template.format(
        depth_distribution=depth_dist,
        requirements_mapping=requirements_mapping_str
    )
    
    llm_result = evaluate_with_llm(prompt_text)
    depth_score = float(llm_result.score)
    llm_reasoning = llm_result.reasoning
    
    # 5. Populate AxisScore
    awarded = max(0.0, coverage_score + depth_score + penalty_points)
    
    return {
        "score_functional": {
            "awarded": awarded,
            "possible": 25,
            "sub_scores": {
                "mapping_coverage": coverage_score,
                "depth_of_resolution": depth_score
            },
            "llm_reasoning": llm_reasoning,
            "penalties_applied": penalties_applied
        }
    }
