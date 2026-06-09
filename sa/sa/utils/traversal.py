from typing import List, Dict, Any

def reconstruct_hierarchy(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    tree = {
        "persons": [],
        "external_systems": [],
        "systems": []
    }
    
    entity_map = {e["id"]: dict(e, children=[]) for e in entities}
    
    for e in entity_map.values():
        c4_type = e.get("c4_type")
        if c4_type == "person":
            tree["persons"].append(e)
        elif c4_type == "external_system":
            tree["external_systems"].append(e)
        elif c4_type == "system":
            tree["systems"].append(e)
        elif c4_type == "container":
            parent_id = e.get("parent_system_id")
            if parent_id and parent_id in entity_map:
                entity_map[parent_id]["children"].append(e)
        elif c4_type == "component":
            parent_id = e.get("parent_container_id")
            if parent_id and parent_id in entity_map:
                entity_map[parent_id]["children"].append(e)
                
    return tree

def get_c4_depth(c4_type: str) -> int:
    mapping = {
        "person": 0,
        "external_system": 0,
        "system": 1,
        "container": 2,
        "component": 3
    }
    return mapping.get(c4_type, 0)

def build_traceability_matrix(entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    matrix = {}
    
    for e in entities:
        req_ids = e.get("requirement_ids", [])
        c4_type = e.get("c4_type", "unknown")
        entity_id = e.get("id")
        
        for req_id in req_ids:
            if req_id not in matrix:
                matrix[req_id] = []
            matrix[req_id].append({
                "entity_id": entity_id,
                "level": c4_type,
            })
            
    for req_id, entries in matrix.items():
        deepest_depth = -1
        deepest_level = "unknown"
        for entry in entries:
            depth = get_c4_depth(entry["level"])
            if depth > deepest_depth:
                deepest_depth = depth
                deepest_level = entry["level"]
                
        for entry in entries:
            entry["deepest_level"] = deepest_level
            
    return matrix

def extract_orphaned_requirements(traceability_matrix: Dict[str, Any], requirements_data: Dict[str, Any]) -> List[str]:
    all_reqs = requirements_data.get("asrs", []) + requirements_data.get("non_asr", [])
    orphans = []
    for req in all_reqs:
        if req not in traceability_matrix or not traceability_matrix[req]:
            orphans.append(req)
    return orphans

def extract_tech_and_patterns(entities: List[Dict[str, Any]]) -> tuple[Dict[str, str], Dict[str, List[str]]]:
    tech_list = {}
    patterns_list = {}
    
    for e in entities:
        entity_id = e.get("id")
        if "technology" in e and e["technology"]:
            tech_list[entity_id] = e["technology"]
        
        metadata = e.get("metadata", {})
        if "patterns" in metadata and metadata["patterns"]:
            patterns_list[entity_id] = metadata["patterns"]
            
    return tech_list, patterns_list
