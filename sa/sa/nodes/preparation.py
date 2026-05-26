from typing import Dict, Any
from sa.state.schemas import SAState
from sa.utils.traversal import (
    build_traceability_matrix,
    extract_orphaned_requirements,
)

def node_preparation(state: SAState) -> Dict[str, Any]:
    arch_model = state.get("arch_model", {})
    entities = arch_model.get("entities", [])
    requirements_data = state.get("requirements_data", {})
    
    traceability_matrix = build_traceability_matrix(entities)
    orphaned_reqs = extract_orphaned_requirements(traceability_matrix, requirements_data)
    
    return {
        "traceability_matrix": traceability_matrix,
        "orphaned_reqs": orphaned_reqs,
    }
