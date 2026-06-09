from typing import Any
from langchain_core.runnables import RunnableConfig
from aga.state.schemas import AGAState

async def input_parsing(state: AGAState, config: RunnableConfig) -> dict[str, Any]:
    """
    Parses the flat JSON arch_model and derives the queue of diagrams.
    Returns updates for diagram_queue and diagram_cursor.
    """
    arch_model = state.get("arch_model", {})
    entities = arch_model.get("entities", [])
    relationships = arch_model.get("relationships", [])
    
    diagram_queue = []
    
    # 1. Process System entities for Context and Container diagrams
    systems = [e for e in entities if e.get("c4_type") == "system"]
    
    for sys_entity in systems:
        sys_id = sys_entity.get("id")
        sys_name = sys_entity.get("name", "")
        
        # --- Context Diagram ---
        ctx_rels = [
            r for r in relationships 
            if r.get("diagram_scope") == "context" and 
            (r.get("source_id") == sys_id or r.get("target_id") == sys_id)
        ]
        
        if ctx_rels:
            involved_ids = {sys_id}
            for r in ctx_rels:
                involved_ids.add(r.get("source_id"))
                involved_ids.add(r.get("target_id"))
                
            ctx_entities = [e for e in entities if e.get("id") in involved_ids]
            
            diagram_queue.append({
                "diagram_id": f"ctx-{sys_id}",
                "diagram_type": "context",
                "focus_entity_id": sys_id,
                "focus_entity_label": sys_name,
                "entities": ctx_entities,
                "relationships": ctx_rels
            })
            
        # --- Container Diagram ---
        system_containers = [e for e in entities if e.get("c4_type") == "container" and e.get("parent_system_id") == sys_id]
        system_container_ids = {c.get("id") for c in system_containers}
        
        cnt_rels = [
            r for r in relationships 
            if r.get("diagram_scope") == "container" and 
            (r.get("source_id") in system_container_ids or r.get("target_id") in system_container_ids)
        ]
        
        if cnt_rels:
            involved_ids = set(system_container_ids)
            for r in cnt_rels:
                involved_ids.add(r.get("source_id"))
                involved_ids.add(r.get("target_id"))
                
            cnt_entities = [e for e in entities if e.get("id") in involved_ids]
            
            diagram_queue.append({
                "diagram_id": f"cnt-{sys_id}",
                "diagram_type": "container",
                "focus_entity_id": sys_id,
                "focus_entity_label": sys_name,
                "entities": cnt_entities,
                "relationships": cnt_rels
            })

    # 2. Process Container entities for Component diagrams
    containers = [e for e in entities if e.get("c4_type") == "container"]
    
    for cnt_entity in containers:
        cnt_id = cnt_entity.get("id")
        cnt_name = cnt_entity.get("name", "")
        
        container_components = [e for e in entities if e.get("c4_type") == "component" and e.get("parent_container_id") == cnt_id]
        container_component_ids = {c.get("id") for c in container_components}
        
        cmp_rels = [
            r for r in relationships 
            if r.get("diagram_scope") == "component" and 
            (r.get("source_id") in container_component_ids or r.get("target_id") in container_component_ids)
        ]
        
        if cmp_rels:
            involved_ids = set(container_component_ids)
            for r in cmp_rels:
                involved_ids.add(r.get("source_id"))
                involved_ids.add(r.get("target_id"))
                
            cmp_entities = [e for e in entities if e.get("id") in involved_ids]
            
            diagram_queue.append({
                "diagram_id": f"cmp-{cnt_id}",
                "diagram_type": "component",
                "focus_entity_id": cnt_id,
                "focus_entity_label": cnt_name,
                "entities": cmp_entities,
                "relationships": cmp_rels
            })
            
    return {
        "diagram_queue": diagram_queue,
        "diagram_cursor": 0
    }
