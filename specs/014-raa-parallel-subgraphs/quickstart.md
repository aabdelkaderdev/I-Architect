# Quickstart: RAA Parallel Subgraphs

This guide demonstrates how to invoke parallel subgraphs and validate parent links in returned fragments.

## 1. Emitting Sends via Conditional Edge

```python
from langgraph.types import Send
from raa.graphs.subgraphs.routing import fan_out_subgraphs

# fan_out_subgraphs reads batch_queue[batch_cursor] and returns Send objects
# with LLM instances from runtime context.
sends = fan_out_subgraphs(state, config)
# Normal batch → [Send("raa_a", {...}), Send("raa_b", {...}), Send("raa_c", {...})]
# Reduced-confidence batch → [Send("raa_a", {...})]
```

## 2. Strategy Subgraph Execution

```python
from raa.graphs.subgraphs.raa_a import run_raa_a
from raa.graphs.subgraphs.raa_b import run_raa_b
from raa.graphs.subgraphs.raa_c import run_raa_c

# Each strategy receives the Send payload and returns batch_outputs
result_a = run_raa_a(payload)
# → {"batch_outputs": {0: [ArchFragment(...)]}}
```

## 3. LLM Injection Pattern

```python
config = {
    "context": {
        "llm_raa_a": chat_model_a,
        "llm_raa_b": chat_model_b,
        "llm_raa_c": chat_model_c,
    }
}
# LLMs injected into Send payloads by fan_out_subgraphs, consumed by strategies
# Never stored in RAAState channels
```

## 4. Parent Link Validation

```python
from raa.graphs.subgraphs.common import validate_parent_links, validate_relationship_scopes

# Ensures no orphan containers or components
validate_parent_links(fragment, running_arch_model)

# Ensures every relationship has a valid diagram_scope matching endpoint types
validate_relationship_scopes(fragment, running_arch_model)
```
