<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_png/PngDrawer/draw -->

Methodv1.2.21 (latest)●Since v0.1

# draw

Draw the given state graph into a PNG file.

Requires `graphviz` and `pygraphviz` to be installed.


```
draw(
  self,
  graph: Graph,
  output_path: str | None = None
) -> bytes | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `graph`\* | `Graph` | The graph to draw |
| `output_path` | `str | None` | Default:`None`  The path to save the PNG. If `None`, PNG bytes are returned. |


