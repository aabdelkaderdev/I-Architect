# Research Report: Parallel Subgraph Orchestration and LLM Injection

This report details parallel routing strategies and context model management.

## 1. LangGraph Send API with Context LLMs

### Decision
Emit `Send` objects containing the strategy node targets and state payloads. Retrieve LLM instances dynamically from the config context at fan-out boundaries:
```python
def fan_out_subgraphs(state, config):
    ctx = config.get("context", {})
    batch = state["batch_queue"][state["batch_cursor"]]
    
    if batch.get("reduced_confidence", False):
        # Incoherent fallback route
        return [Send("raa_a", {"batch": batch, "llm": ctx.get("llm_raa_a")})]
        
    return [
        Send("raa_a", {"batch": batch, "llm": ctx.get("llm_raa_a")}),
        Send("raa_b", {"batch": batch, "llm": ctx.get("llm_raa_b")}),
        Send("raa_c", {"batch": batch, "llm": ctx.get("llm_raa_c")}),
    ]
```

### Rationale
This architecture dynamically overrides the execution routing without polluting checkpoint states or violating checkpoint serialization restrictions.

---

## 2. Parent-Child Validation Rules

### Decision
Perform schema checks on the output list of systems, containers, and components:
- If a component is created, check if its `parent_container_id` references a container present in the same fragment or the `running_arch_model`.
- If a container is created, check if its `parent_system_id` references a system present in the same fragment or the `running_arch_model`.

### Rationale
This validation guarantees that every entity is properly mapped in the C4 hierarchy before entering the judge's merge phase.
