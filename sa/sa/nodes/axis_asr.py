from typing import Dict, Any
import os
from sa.state.schemas import SAState
from sa.utils.llm import evaluate_with_llm
from sa.utils.traversal import extract_tech_and_patterns

def node_asr(state: SAState) -> Dict[str, Any]:
    req_data = state.get("requirements_data", {})
    asrs = req_data.get("asrs", [])
    total_asrs = len(asrs)
    
    traceability_matrix = state.get("traceability_matrix", {})
    
    # 1. Deterministic mapping coverage
    mapped_asrs = sum(1 for req in asrs if req in traceability_matrix and traceability_matrix[req])
    
    if total_asrs > 0:
        coverage_score = (mapped_asrs / total_asrs) * 15.0
    else:
        coverage_score = 0.0
        
    # Extract technologies and patterns
    arch_model = state.get("arch_model", {})
    entities = arch_model.get("entities", [])
    tech_list, patterns_list = extract_tech_and_patterns(entities)
    
    # 2. Deterministic contradiction penalty
    contradictions_found = 0
    penalties_applied = []
    
    for req in asrs:
        if req in traceability_matrix and traceability_matrix[req]:
            # Simple heuristic for contradiction: req has 'async' but pattern is 'sync'
            req_lower = req.lower()
            for entry in traceability_matrix[req]:
                eid = entry.get("entity_id")
                entity_patterns = patterns_list.get(eid, [])
                
                is_sync_pattern = any("sync" in p.lower() and "async" not in p.lower() for p in entity_patterns)
                if "async" in req_lower and is_sync_pattern:
                    contradictions_found += 1
                    penalties_applied.append({
                        "reason": f"Contradiction: ASR '{req}' requires async, but entity '{eid}' uses a synchronous pattern.",
                        "points": -5.0,
                        "requirement_id": req
                    })
                    
    penalty_points = contradictions_found * -5.0
    
    # 3. LLM call for Technology Specificity
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "technology_specificity.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    else:
        prompt_template = "ASRs: {asr_requirements}\nTechnologies: {technology_list}"
        
    tech_list_str = "\n".join([f"- Entity {k}: {v}" for k, v in tech_list.items()]) if tech_list else "None"
    asr_str = "\n".join([f"- {req}" for req in asrs]) if asrs else "None"
    
    prompt_text = prompt_template.format(
        asr_requirements=asr_str,
        technology_list=tech_list_str
    )
    
    llm_result = evaluate_with_llm(prompt_text)
    specificity_score = float(llm_result.score)
    llm_reasoning = llm_result.reasoning
    
    # 4. Populate AxisScore
    awarded = max(0.0, coverage_score + specificity_score + penalty_points)
    
    return {
        "score_asr": {
            "awarded": awarded,
            "possible": 25,
            "sub_scores": {
                "asr_mapping_coverage": coverage_score,
                "technology_specificity": specificity_score
            },
            "llm_reasoning": llm_reasoning,
            "penalties_applied": penalties_applied
        }
    }
