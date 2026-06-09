# Product Requirements Document
## Architecture Generation Agent (AGA) — Phase 3: RAA Normalisation & Diagram Queue Builder
**Version:** 1.0
**Status:** Draft
**Scope:** The thin adapter layer that converts the raw RAA output dict into the AGA's typed `RAAOutput`, and the pure-function queue builder that derives the ordered `list[DiagramSpec]` from it. These two concerns are tightly coupled — the queue builder cannot run without a parsed `RAAOutput` — so they are specified together in this phase.

---

## 1. Overview

The Orchestrator passes the RAA output as a plain `dict` to the AGA graph. Before any diagram work can begin, two deterministic (non-LLM) steps must execute:

1. **Normalisation** — parse and validate the raw dict into the typed `RAAOutput` defined in Phase 2.
2. **Queue building** — traverse the `RAAOutput` to produce the ordered `list[DiagramSpec]` that drives the agent loop.

Both steps are pure functions with no I/O, no LLM calls, and no side effects. They live in dedicated modules so they can be unit-tested in isolation.

---

## 2. Files Created in This Phase

| File | Purpose |
|------|---------|
| `aga/normaliser.py` | `normalise_raa_output(raw: dict) → RAAOutput` — parse and validate the raw RAA dict |
| `aga/queue_builder.py` | `build_diagram_queue(raa: RAAOutput) → list[DiagramSpec]` — derive the ordered work queue |

`aga/graph.py` is updated to wire these as two sequential nodes that run after `START` and before the agent loop node (which is added in Phase 6).

---

## 3. `aga/normaliser.py` — RAA Normalisation

### 3.1 Purpose

The raw RAA output is a plain Python `dict` — it is not Pydantic-validated at the AGA boundary. The normaliser converts it into the typed `RAAOutput` defined in Phase 2 (`aga/schemas.py`), making all downstream code type-safe and IDE-navigable.

### 3.2 Signature

```python
def normalise_raa_output(raw: dict) -> RAAOutput:
    """
    Parse and validate the raw RAA output dict into a typed RAAOutput.

    Parameters
    ----------
    raw : dict
        The plain dict exactly as returned by the RAA graph.

    Returns
    -------
    RAAOutput
        Fully typed representation of the RAA output.

    Raises
    ------
    NormalisationError
        If a required top-level key is missing or a sub-structure cannot
        be parsed into its expected type.
    """
```

### 3.3 `NormalisationError`

A module-local exception class (subclass of `ValueError`) raised when the raw dict does not conform to the expected structure.

```python
class NormalisationError(ValueError):
    """Raised when the RAA output dict cannot be parsed into RAAOutput."""
```

It carries the failing key path (e.g. `"l2_descriptions[2].containers[0].canonical_id"`) as the message to aid debugging without exposing stack traces to the Orchestrator.

### 3.4 Parsing Strategy

The normaliser uses Pydantic's `model_validate` on each RAA boundary type defined in Phase 2 (`schemas.py`). This is the simplest approach: each sub-dict is passed directly to the corresponding Pydantic model's constructor, which handles field coercion and missing-field defaults automatically.

**Step-by-step:**

1. Assert the four required top-level keys exist: `"l1_description"`, `"l2_descriptions"`, `"l3_descriptions"`, `"entity_registry"`. Raise `NormalisationError` if any is absent.
2. Parse `raw["l1_description"]` → `RAAL1Description.model_validate(...)`.
3. Parse each item in `raw["l2_descriptions"]` → `RAAL2Description.model_validate(...)`. Collect into a list.
4. Parse each item in `raw["l3_descriptions"]` → `RAAL3Description.model_validate(...)`. Collect into a list.
5. Parse each value in `raw["entity_registry"]` → `RAAEntityRegistryEntry.model_validate(...)`. Collect into `dict[str, RAAEntityRegistryEntry]`.
6. Pass `coverage_gaps` and `conflicts` through as raw `list[dict]` — no parsing.
7. Construct and return `RAAOutput(...)`.

Any `pydantic.ValidationError` raised during steps 2–5 is caught and re-raised as `NormalisationError` with the offending path embedded in the message.

### 3.5 Design Notes

- The normaliser does **not** validate business rules (e.g. "every `L3Description` must reference a `parent_container_id` that exists in the entity registry"). Business validation is the RAA's responsibility. The normaliser only checks that fields exist and are the right Python type.
- The normaliser is a **pure function** — no side effects, no I/O, no module-level state.
- It is intentionally strict on required fields and permissive on optional/unknown fields (`model_config = ConfigDict(extra="ignore")` on boundary types). Unknown fields are ignored rather than preserved in AGA state; this keeps downstream prompts and sidecars stable if the RAA adds fields in future versions.

---

## 4. `aga/queue_builder.py` — Diagram Queue Builder

### 4.1 Purpose

Given a fully-parsed `RAAOutput`, produce the ordered `list[DiagramSpec]` that the agent loop processes one entry at a time. The queue builder contains no LLM calls, no I/O, and no randomness — it is a deterministic traversal of the `RAAOutput` structure.

### 4.2 Signature

```python
def build_diagram_queue(raa: RAAOutput) -> list[DiagramSpec]:
    """
    Derive the ordered diagram work queue from a parsed RAAOutput.

    The queue ordering is:
        1. One context diagram (from l1_description)
        2. One container diagram per l2_descriptions entry (in list order)
        3. One component diagram per l3_descriptions entry (in list order)

    Parameters
    ----------
    raa : RAAOutput
        Fully parsed RAA output (output of normalise_raa_output).

    Returns
    -------
    list[DiagramSpec]
        Ordered list of diagram specifications. Never empty — at minimum
        one context diagram is always present.
    """
```

### 4.3 Queue Derivation Rules

The queue is built in three passes, always in this fixed order:

#### Pass 1 — Context Diagram (always exactly 1)

Source: `raa.l1_description`

```
diagram_id     = "ctx"
diagram_type   = "context"
label          = f"System Context — {raa.l1_description.system_name}"
output_filename = "ctx.png"
source_l1      = raa.l1_description
source_l2      = None
source_l3      = None
```

#### Pass 2 — Container Diagrams (one per L2 entry)

Source: `raa.l2_descriptions`, iterated in list order.

For each `l2` in `raa.l2_descriptions`:

```
diagram_id      = f"cnt-{l2.concern_id}"
diagram_type    = "container"
label           = f"Container Diagram — {l2.concern_id}"
output_filename = f"cnt-{l2.concern_id}.png"
source_l1       = None
source_l2       = l2
source_l3       = None
```

#### Pass 3 — Component Diagrams (one per L3 entry)

Source: `raa.l3_descriptions`, iterated in list order.

For each `l3` in `raa.l3_descriptions`:

```
diagram_id      = f"cmp-{l3.parent_container_id}-{l3.concern_id}"
diagram_type    = "component"
label           = f"Component Diagram — {l3.parent_container_id} ({l3.concern_id})"
output_filename = f"cmp-{l3.parent_container_id}-{l3.concern_id}.png"
source_l1       = None
source_l2       = None
source_l3       = l3
```

### 4.4 `diagram_id` Collision Handling

It is possible (though unlikely in practice) for two `l2_descriptions` entries to share the same `concern_id`, or two `l3_descriptions` entries to share the same `parent_container_id`-`concern_id` pair. This would produce duplicate `diagram_id` values.

**Resolution rule:** If a collision is detected, append a zero-based integer suffix to the later entry's `diagram_id` and `output_filename`:

```
cnt-concern_batch_2        → first occurrence, unchanged
cnt-concern_batch_2-1      → second occurrence
cmp-svc_auth-batch_2       → first occurrence, unchanged
cmp-svc_auth-batch_2-1     → second occurrence (if any)
```

Collisions do not raise an exception — the queue is still returned with suffixed IDs. The suffix itself is the observable signal; the pure queue builder does not perform logging or any other side effect.

### 4.5 Design Notes

- The queue builder is a **pure function** — given the same `RAAOutput` it always returns the same queue in the same order.
- It does **not** filter entries (e.g. it does not skip L3 entries with empty `components` lists). Empty diagrams are valid inputs for the agent — the agent will generate a minimal valid PlantUML stub. Filtering is the agent's concern, not the queue builder's.
- The total queue length is always: `1 + len(raa.l2_descriptions) + len(raa.l3_descriptions)`.

---

## 5. LangGraph Node Wiring (update to `graph.py`)

Two new nodes are added to `graph.py` in this phase, running sequentially before the agent loop:

### 5.1 `normalise_node`

```python
def normalise_node(state: AGAInputState) -> dict:
    parsed = normalise_raa_output(state["raa_output"])
    return {
        "parsed_raa": parsed,
        "completed_diagrams": [],
        "failed_diagrams": [],
    }
```

### 5.2 `build_queue_node`

```python
def build_queue_node(state: AGAInternalState) -> dict:
    queue = build_diagram_queue(state["parsed_raa"])
    import time
    return {
        "diagram_queue": queue,
        "session_start_time": time.time(),
    }
```

### 5.3 Edge additions to `builder`

```python
builder.add_node("normalise", normalise_node)
builder.add_node("build_queue", build_queue_node)

builder.add_edge(START, "normalise")
builder.add_edge("normalise", "build_queue")
builder.add_edge("build_queue", END)   # placeholder; replaced in Phase 6
```

---

## 6. Unit Test Criteria

### Normaliser

- Given the reference `raa_output.pkl` dict, `normalise_raa_output` returns an `RAAOutput` with `len(raa.l2_descriptions) == 4` and `len(raa.l3_descriptions) == 2` (matching the fixture).
- A dict missing the `"l1_description"` key raises `NormalisationError`.
- A dict where `l2_descriptions[0]["containers"][0]` is missing `"canonical_id"` raises `NormalisationError` with a message mentioning the path.
- Unknown extra keys in the raw dict are silently ignored (no error).

### Queue Builder

- Given a fixture `RAAOutput` with 1 L1, 4 L2 entries, 2 L3 entries, the queue has exactly 7 `DiagramSpec` items in the order: 1 context, 4 container, 2 component.
- The context `DiagramSpec` has `diagram_id == "ctx"` and `source_l1 is not None` and `source_l2 is None` and `source_l3 is None`.
- Each container `DiagramSpec` has `diagram_type == "container"` and exactly one non-null source field (`source_l2`).
- Each component `DiagramSpec` has `diagram_type == "component"` and exactly one non-null source field (`source_l3`).
- Two L2 entries with the same `concern_id` produce `diagram_id` values `"cnt-{id}"` and `"cnt-{id}-1"` respectively.
- Two L3 entries with the same `parent_container_id` and `concern_id` produce `diagram_id` values `"cmp-{pid}-{cid}"` and `"cmp-{pid}-{cid}-1"` respectively.

---

## 7. Design Constraints Summary

| Constraint | Rule |
|------------|------|
| Normaliser purity | No I/O, no side effects, no LLM calls |
| Queue builder purity | Deterministic; same input always produces same output |
| Queue ordering | Context first, then containers (L2 order), then components (L3 order) |
| Collision handling | Suffix deduplication; no exception raised |
| Business validation | Not the normaliser's job — RAA guarantees structural correctness |
| Empty L3 entries | Not filtered — passed to agent as-is |
| Queue minimum size | Always ≥ 1 (the context diagram is always present) |

---

## 8. What This Phase Defers

| Concern | Phase |
|---------|-------|
| `@tool` adapter for `render_plantuml` | Phase 4 |
| Mustache prompt template revision | Phase 5 |
| Agent loop node, retry logic, output assembly | Phase 6 |
