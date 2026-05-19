# Quickstart: RAA LangGraph Skeleton

This guide demonstrates how to build, compile, and run the main RAA LangGraph skeleton.

## 1. Build and Compile the Graph

```python
from raa.graphs.main_graph import build_raa_graph, compile_raa_graph

# Build the uncompiled StateGraph (injectable node overrides for testing)
graph = build_raa_graph()

# Compile to an invokable app (no checkpointer required)
app = compile_raa_graph()
```

## 2. Invocation

```python
inputs = {
    "requirements": [{"id": "1", "content": "Security system"}],
    "condition_groups": {"group_1": ["1"]},
    "embeddings_ready": True,
}

output = app.invoke(inputs)
print(output["batch_queue"])
```

## 3. Testing with Mock Nodes

```python
from unittest.mock import MagicMock

mock_nodes = {
    "prepare_embeddings": MagicMock(return_value={"embeddings_ready": True}),
    "construct_batches": MagicMock(return_value={"batch_queue": [{"id": "B1"}]}),
    "apply_overlap_bridging": MagicMock(return_value={"batch_queue": [{"id": "B1"}]}),
    "apply_coherence_gate": MagicMock(return_value={"batch_queue": [{"id": "B1"}]}),
    "order_batch_queue": MagicMock(return_value={"batch_queue": [{"id": "B1", "order": 1}]}),
}

app = compile_raa_graph(node_overrides=mock_nodes)
result = app.invoke({"embeddings_ready": True})
assert result["batch_queue"] == [{"id": "B1", "order": 1}]
```

## 4. Embeddings-Ready Gate Behavior

```python
# Raises ValueError when embeddings_ready is False
try:
    app = compile_raa_graph()
    app.invoke({"embeddings_ready": False})
except ValueError as e:
    print(f"Gate halted: {e}")
```
