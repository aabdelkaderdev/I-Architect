from typing import TypedDict, List, Dict, Any, Optional
from sa.state.models import AxisScore, ScoringReport

class SAState(TypedDict):
    arch_model: dict
    plantuml_context: str
    plantuml_container: str
    plantuml_component: str
    requirements_data: dict
    traceability_matrix: dict
    orphaned_reqs: List[str]
    score_functional: AxisScore
    score_asr: AxisScore
    score_saam: AxisScore
    final_report: ScoringReport
    output_path: str
    diagram_issues: List[Any]
