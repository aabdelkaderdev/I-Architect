<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_png/PngDrawer/add_edge -->

Methodv1.2.21 (latest)●Since v0.1

# add\_edge

Adds an edge to the graph.


```
add_edge(
  self,
  viz: Any,
  source: str,
  target: str,
  label: str | None = None,
  conditional: bool = False
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `viz`\* | `Any` | The graphviz object. |
| `source`\* | `str` | The source node. |
| `target`\* | `str` | The target node. |
| `label` | `str | None` | Default:`None`  The label for the edge. |
| `conditional` | `bool` | Default:`False`  Whether the edge is conditional. |


