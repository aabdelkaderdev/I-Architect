# Data Model: Subgraph Strategy Payload and ArchFragment

This feature uses the authoritative `ArchFragment` dataclass from `raa/state/types.py` and the `RAAState` channels from `raa/state/channels.py`. No duplicate type definitions are introduced.

## 1. SubgraphInputPayload (Send payload)

Passed from the routing edge to each strategy subgraph node via LangGraph `Send`.

```python
from typing import TypedDict, Any

class SubgraphPayload(TypedDict, total=False):
    batch: dict  # Current batch from batch_queue
    batch_index: int
    quality_weights: dict[str, int]
    running_arch_model: dict | None  # Serializable form of ArchModel
    bridge_requirements: dict[tuple, list[str]]
    strategy: str  # "saam_first" | "pattern_driven" | "entity_driven"
    llm: Any  # ChatModel injected from runtime context (NOT stored in state)
```

## 2. ArchFragment Output

Each subgraph returns `{"batch_outputs": {batch_index: [ArchFragment(...)]}}`.

The `ArchFragment` dataclass (from `raa/state/types.py`) contains:
- `systems: list[ArchSystem]` — each has `id`, `label`, `description`
- `containers: list[ArchContainer]` — each has `id`, `label`, `description`, `parent_system_id`
- `components: list[ArchComponent]` — each has `id`, `label`, `description`, `parent_container_id`
- `persons: list[ArchPerson]` — flat leaf entities
- `external_systems: list[ArchExternalSystem]` — flat leaf entities
- `relationships: list[ArchRelationship]` — each has `diagram_scope` ∈ {`context`, `container`, `component`}
- `patterns: list[ArchPattern]`
- `rationale: dict`

## 3. Relationship Scoping Rules (Section 12)

| Source Type | Target Type | `diagram_scope` |
|-------------|-------------|-----------------|
| System, Person, ExternalSystem | System, Person, ExternalSystem | `context` |
| Container | Container | `container` |
| Component | Component | `component` |

Cross-scope relationships are invalid and rejected by `validate_relationship_scopes`.
