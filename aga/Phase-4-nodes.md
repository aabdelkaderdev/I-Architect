# Phase 4 — Diagram Resolution & Input Nodes

> **Goal:** Build the diagram scope resolution logic that derives the diagram work queue from the flat JSON input, plus the two entry-point nodes: `server_guard` (PlantUML server availability check) and `input_parsing` (flat JSON → DiagramSpec queue).
>
> **Depends on:** Phase 1 (state models: `DiagramSpec`, `AGAState`, `AGAConfig`), Phase 2 (tools: used indirectly by server_guard for HTTP)
> **Produces:** `aga/nodes/server_guard.py`, `aga/nodes/input_parsing.py`, `aga/nodes/__init__.py`
> **Test fixture:** `arch_model_test_result-1.json`

---

## 3) Diagram Scope Resolution Strategy

### 3A — Manifest Derivation from Flat Input

Since the flat JSON does not include a pre-built `diagram_manifest`, the AGA must **derive the diagram work queue** from the input data:

1. **Collect unique systems:** Scan entities where `c4_type = "system"`. Each system produces a potential context diagram and a potential container diagram.
2. **Collect unique containers:** Scan entities where `c4_type = "container"`. Each container (with components inside it) produces a potential component diagram.
3. **Scope-filter relationships:** Group relationships by `diagram_scope`. Only generate a diagram if at least one relationship exists for that scope + focus entity combination.

### 3B — Focus Entity Resolution per Diagram Type

| Diagram Type | Focus Entity | Included Entities | Included Relationships |
|-------------|-------------|-------------------|----------------------|
| **Context** | A `system` entity | The focus system + all persons, external systems, and other systems referenced in `diagram_scope = "context"` relationships involving the focus system | All relationships where `diagram_scope = "context"` and either `source_id` or `target_id` matches the focus system or its related actors |
| **Container** | A `system` entity | All containers with `parent_system_id` matching the focus system + persons and external systems referenced in `diagram_scope = "container"` relationships | All relationships where `diagram_scope = "container"` involving containers of the focus system |
| **Component** | A `container` entity | All components with `parent_container_id` matching the focus container + other containers or external systems referenced in `diagram_scope = "component"` relationships | All relationships where `diagram_scope = "component"` involving components of the focus container |

### 3C — Diagram ID Convention

Derived diagram IDs follow the stable canonical pattern:

- Context: `ctx-{system_id}` (e.g., `ctx-sys1`)
- Container: `cnt-{system_id}` (e.g., `cnt-sys1`)
- Component: `cmp-{container_id}` (e.g., `cmp-container2`)

### 3D — Output Filename Convention

- PNG files: `{diagram_id}.png` (e.g., `ctx-sys1.png`)
- PlantUML source: `{diagram_id}.puml` (e.g., `ctx-sys1.puml`)
- Metadata sidecar: `{diagram_id}_metadata.json`

---

## Node: `server_guard`

From §7B Graph Topology:

```
START
  │
  ▼
[server_guard]          ── HEAD check PlantUML server availability
```

- Performs a HEAD request to the PlantUML server base URL
- On success: proceed to `input_parsing`
- On failure: raise `ServerUnavailableException` and halt immediately

From §12 Error Handling:

| Error Type | Source | Agent Response |
|------------|--------|----------------|
| `ServerUnavailableException` | HEAD check failed | **Halt immediately** — no diagrams attempted |

---

## Node: `input_parsing`

From §7B Graph Topology:

```
[server_guard]
  │
  ▼
[input_parsing]         ── Parse flat JSON → derive diagram queue
```

- Reads `arch_model` from state
- Applies the Manifest Derivation logic (§3A)
- Applies Focus Entity Resolution (§3B)
- Generates ordered `diagram_queue` of `DiagramSpec` objects
- Sets `diagram_cursor = 0`

---

## Relevant Validation Criteria (from §15)

### Unit Tests
- Diagram queue derivation from flat JSON produces correct count and ordering

### Integration Tests
- End-to-end with `arch_model_test_result-1.json`: agent generates all derivable diagrams
