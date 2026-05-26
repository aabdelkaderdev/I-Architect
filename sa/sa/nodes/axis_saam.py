import os
import json
from typing import Dict, Any, List

from sa.state.schemas import SAState
from sa.utils.plantuml_parser import parse_c4_plantuml
from sa.utils.llm import evaluate_saam_with_llm

def node_saam(state: SAState) -> Dict[str, Any]:
    # 1. Diagram Verification (Deterministic) - Max 20 points
    diagram_score = 20.0
    diagram_issues = []
    
    puml_context = state.get("plantuml_context", "")
    puml_container = state.get("plantuml_container", "")
    puml_component = state.get("plantuml_component", "")
    
    # 3.1 Render completeness
    empty_deduction = 20.0 / 3.0
    render_completeness_score = 20.0
    
    for name, puml in [("Context", puml_context), ("Container", puml_container), ("Component", puml_component)]:
        if not puml or not puml.strip():
            diagram_issues.append({
                "diagram_type": name,
                "issue_type": "empty_diagram",
                "entity_id": None,
                "description": f"{name} diagram is empty."
            })
            diagram_score -= empty_deduction
            render_completeness_score -= empty_deduction
            
    # Parse diagrams
    context_entities = parse_c4_plantuml(puml_context)
    container_entities = parse_c4_plantuml(puml_container)
    component_entities = parse_c4_plantuml(puml_component)
    
    context_aliases = {e["alias"] for e in context_entities}
    container_aliases = {e["alias"] for e in container_entities}
    component_aliases = {e["alias"] for e in component_entities}
    
    # Check expected entities from arch_model
    arch_model = state.get("arch_model", {})
    expected_entities = arch_model.get("entities", [])
    
    # We will deduct 0.5 points per missing/misplaced entity
    deduction_per_issue = 0.5
    entity_inclusion_score = 0.0
    hierarchy_validity_score = 0.0
    
    expected_context = 0
    expected_container = 0
    expected_component = 0
    
    for e in expected_entities:
        eid = e.get("id")
        c4_type = e.get("c4_type")
        
        # 3.2 Entity inclusion & 3.3 Hierarchy validity
        if c4_type in ["person", "system", "external_system"]:
            expected_context += 1
            if eid not in context_aliases:
                diagram_issues.append({
                    "diagram_type": "Context",
                    "issue_type": "missing_entity",
                    "entity_id": eid,
                    "description": f"Expected {c4_type} '{eid}' is missing from Context diagram."
                })
                diagram_score -= deduction_per_issue
                entity_inclusion_score -= deduction_per_issue
            if eid in container_aliases or eid in component_aliases:
                diagram_issues.append({
                    "diagram_type": "Other",
                    "issue_type": "wrong_level",
                    "entity_id": eid,
                    "description": f"{c4_type} '{eid}' found in lower-level diagram."
                })
                diagram_score -= deduction_per_issue
                hierarchy_validity_score -= deduction_per_issue
                
        elif c4_type == "container":
            expected_container += 1
            if eid not in container_aliases:
                diagram_issues.append({
                    "diagram_type": "Container",
                    "issue_type": "missing_entity",
                    "entity_id": eid,
                    "description": f"Expected container '{eid}' is missing from Container diagram."
                })
                diagram_score -= deduction_per_issue
                entity_inclusion_score -= deduction_per_issue
                
        elif c4_type == "component":
            expected_component += 1
            if eid not in component_aliases:
                diagram_issues.append({
                    "diagram_type": "Component",
                    "issue_type": "missing_entity",
                    "entity_id": eid,
                    "description": f"Expected component '{eid}' is missing from Component diagram."
                })
                diagram_score -= deduction_per_issue
                entity_inclusion_score -= deduction_per_issue
                
    diagram_score = max(0.0, diagram_score)

    # 4. SAAM Evaluation (LLM) - Max 30 points
    req_data = state.get("requirements_data", {})
    asrs = req_data.get("asrs", [])
    qa_list = [f"- {asr}" for asr in asrs]
    qa_str = "\n".join(qa_list) if qa_list else "None specified"
    
    # Extract patterns and technologies
    tech_patterns = []
    for e in expected_entities:
        eid = e.get("id")
        tech = e.get("technology", "None")
        meta = e.get("metadata", {})
        patterns = meta.get("patterns", [])
        if tech != "None" or patterns:
            tech_patterns.append(f"Entity '{eid}': Tech={tech}, Patterns={patterns}")
            
    patterns_str = "\n".join(tech_patterns) if tech_patterns else "None specified"
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "saam_validation.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as f:
            prompt_template = f.read()
    else:
        prompt_template = "QA: {quality_attributes}\nPatterns: {patterns_and_technologies}"
        
    prompt_text = prompt_template.format(
        quality_attributes=qa_str,
        patterns_and_technologies=patterns_str
    )
    
    # Call LLM
    saam_result = evaluate_saam_with_llm(prompt_text)
    saam_score = max(0, min(30, float(saam_result.score)))
    llm_reasoning = saam_result.reasoning
    
    # 5. Output Structure and Reporting
    total_awarded = diagram_score + saam_score
    
    return {
        "score_saam": {
            "awarded": total_awarded,
            "possible": 50,
            "sub_scores": {
                "saam_evaluation": saam_score,
                "render_completeness": render_completeness_score,
                "entity_inclusion": entity_inclusion_score,
                "hierarchy_validity": hierarchy_validity_score
            },
            "llm_reasoning": llm_reasoning,
            "penalties_applied": diagram_issues # We store diagram issues in penalties temporarily to expose them or we can put them in state directly
        },
        # Actually, diagram_issues should go into GapAnalysis. We will pass it in state so report node can pick it up.
        "diagram_issues": diagram_issues
    }
