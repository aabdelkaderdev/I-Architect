<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_mermaid/draw_mermaid -->

Functionv1.2.21 (latest)●Since v0.1

# draw\_mermaid

Draws a Mermaid graph using the provided graph data.


```
draw_mermaid(
  nodes: dict[str, Node],
  edges: list[Edge],
  *,
  first_node: str | None = None,
  last_node: str | None = None,
  with_styles: bool = True,
  curve_style: CurveStyle = CurveStyle.LINEAR,
  node_styles: NodeStyles | None = None,
  wrap_label_n_words: int = 9,
  frontmatter_config: dict[str, Any] | None = None
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `nodes`\* | `dict[str, Node]` | List of node ids. |
| `edges`\* | `list[Edge]` | List of edges, object with a source, target and data. |
| `first_node` | `str | None` | Default:`None`  Id of the first node. |
| `last_node` | `str | None` | Default:`None`  Id of the last node. |
| `with_styles` | `bool` | Default:`True`  Whether to include styles in the graph. |
| `curve_style` | `CurveStyle` | Default:`CurveStyle.LINEAR`  Curve style for the edges. |
| `node_styles` | `NodeStyles | None` | Default:`None`  Node colors for different types. |
| `wrap_label_n_words` | `int` | Default:`9`  Words to wrap the edge labels. |
| `frontmatter_config` | `dict[str, Any] | None` | Default:`None`  Mermaid frontmatter config. Can be used to customize theme and styles. Will be converted to YAML and added to the beginning of the mermaid graph.  See more here: <https://mermaid.js.org/config/configuration.html>.  Example config:   ``` {     "config": {         "theme": "neutral",         "look": "handDrawn",         "themeVariables": {"primaryColor": "#e2e2e2"},     } } ``` |


