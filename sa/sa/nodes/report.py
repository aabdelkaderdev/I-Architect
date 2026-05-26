import json
import os
from typing import Dict, Any
from datetime import datetime
from sa.state.schemas import SAState
from sa.state.models import ScoringReport
from sa.utils.llm import generate_executive_summary_with_llm

def calculate_grade(total_score: float) -> str:
    if total_score >= 90: return "A"
    if total_score >= 80: return "B"
    if total_score >= 70: return "C"
    if total_score >= 60: return "D"
    return "F"

def node_report(state: SAState) -> Dict[str, Any]:
    score_functional = state.get("score_functional", {})
    score_asr = state.get("score_asr", {})
    score_saam = state.get("score_saam", {})
    
    total_score = (
        score_functional.get("awarded", 0.0) +
        score_asr.get("awarded", 0.0) +
        score_saam.get("awarded", 0.0)
    )
    grade = calculate_grade(total_score)
    
    req_data = state.get("requirements_data", {})
    asrs = req_data.get("asrs", [])
    non_asr = req_data.get("non_asr", [])
    total_reqs = len(asrs) + len(non_asr)
    
    orphans = state.get("orphaned_reqs", [])
    diagram_issues = state.get("diagram_issues", [])
    
    # Load prompt template
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "executive_summary.md")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Format summaries for the prompt
    axis1_summary = f"Score: {score_functional.get('awarded', 0)} / {score_functional.get('possible', 0)}"
    if score_functional.get("llm_reasoning"):
        axis1_summary += f"\nReasoning: {score_functional['llm_reasoning']}"
        
    axis2_summary = f"Score: {score_asr.get('awarded', 0)} / {score_asr.get('possible', 0)}"
    if score_asr.get("llm_reasoning"):
        axis2_summary += f"\nReasoning: {score_asr['llm_reasoning']}"
        
    axis3_summary = f"Score: {score_saam.get('awarded', 0)} / {score_saam.get('possible', 0)}"
    if score_saam.get("llm_reasoning"):
        axis3_summary += f"\nReasoning: {score_saam['llm_reasoning']}"

    orphaned_text = json.dumps(orphans, indent=2) if orphans else "None"
    diagram_issues_text = json.dumps(diagram_issues, indent=2) if diagram_issues else "None"

    prompt_text = prompt_template.format(
        total_score=total_score,
        grade=grade,
        axis1_summary=axis1_summary,
        axis2_summary=axis2_summary,
        axis3_summary=axis3_summary,
        orphaned_requirements=orphaned_text,
        diagram_issues=diagram_issues_text
    )

    # Call LLM
    exec_summary_result = generate_executive_summary_with_llm(prompt_text, grade)
    
    report: ScoringReport = {
        "schema_version": "1.0",
        "report_id": "report-1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pipeline_run_id": "run-1",
        "summary": {
            "total_score": total_score,
            "grade": grade,
            "requirements_total": total_reqs,
            "requirements_asr": len(asrs),
            "requirements_functional": len(non_asr),
            "requirements_orphaned": len(orphans),
            "diagrams_present": 0, # Could compute this based on non-empty PUMLs
        },
        "axis_scores": {
            "functional": score_functional,
            "asr_coverage": score_asr,
            "saam_diagrams": score_saam,
        },
        "gap_analysis": {
            "orphaned_requirements": orphans,
            "diagram_issues": diagram_issues
        },
        "executive_summary": {
            "markdown": exec_summary_result.markdown,
            "key_findings": exec_summary_result.key_findings,
            "overall_grade": exec_summary_result.overall_grade
        }
    }
    
    full_markdown = f"""# Scoring Report

{exec_summary_result.markdown}

## Key Findings
"""
    for finding in exec_summary_result.key_findings:
        full_markdown += f"- {finding}\n"
        
    full_markdown += f"""
## Score Breakdown
- **Axis 1 (Functional):** {score_functional.get('awarded', 0)} / {score_functional.get('possible', 0)}
- **Axis 2 (ASR):** {score_asr.get('awarded', 0)} / {score_asr.get('possible', 0)}
- **Axis 3 (SAAM):** {score_saam.get('awarded', 0)} / {score_saam.get('possible', 0)}
- **Total Score:** {total_score} / 100
- **Overall Grade:** {grade}

## Gap Analysis Highlights
- **Orphaned Requirements:** {len(orphans)}
- **Diagram Issues:** {len(diagram_issues)}
"""
    
    output_path = state.get("output_path", ".")
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Output directory does not exist: {output_path}")
    if not os.access(output_path, os.W_OK):
        raise PermissionError(f"Output directory is not writable: {output_path}")
        
    with open(os.path.join(output_path, "scoring_report.json"), "w") as f:
        json.dump(report, f, indent=2)
        
    with open(os.path.join(output_path, "scoring_report.md"), "w") as f:
        f.write(full_markdown)
        
    return {"final_report": report}
