<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_png/PngDrawer -->

Classv1.2.21 (latest)●Since v0.1

# PngDrawer

Helper class to draw a state graph into a PNG file.

It requires `graphviz` and `pygraphviz` to be installed.


```
PngDrawer(
  self,
  fontname: str | None = None,
  labels: LabelsDict | None = None
)
```

**Example:**

```
drawer = PngDrawer()
drawer.draw(state_graph, "graph.png")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `fontname` | `str | None` | Default:`None`  The font to use for the labels. Defaults to "arial". |
| `labels` | `LabelsDict | None` | Default:`None`  A dictionary of label overrides. The dictionary should have the following format: { "nodes": { "node1": "CustomLabel1", "node2": "CustomLabel2", "**end**": "End Node" }, "edges": { "continue": "ContinueLabel", "end": "EndLabel" } } The keys are the original labels, and the values are the new labels. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| fontname | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| labels | [LabelsDict](/python/langchain-core/runnables/graph/LabelsDict) | None |

## Attributes

[attribute

fontname](/python/langchain-core/runnables/graph_png/PngDrawer/fontname)[attribute

labels](/python/langchain-core/runnables/graph_png/PngDrawer/labels)

## Methods

[method

get\_node\_label

Returns the label to use for a node.](/python/langchain-core/runnables/graph_png/PngDrawer/get_node_label)[method

get\_edge\_label

Returns the label to use for an edge.](/python/langchain-core/runnables/graph_png/PngDrawer/get_edge_label)[method

add\_node

Adds a node to the graph.](/python/langchain-core/runnables/graph_png/PngDrawer/add_node)[method

add\_edge

Adds an edge to the graph.](/python/langchain-core/runnables/graph_png/PngDrawer/add_edge)[method

draw

Draw the given state graph into a PNG file.

Requires `graphviz` and `pygraphviz` to be installed.](/python/langchain-core/runnables/graph_png/PngDrawer/draw)[method

add\_nodes

Add nodes to the graph.](/python/langchain-core/runnables/graph_png/PngDrawer/add_nodes)[method

add\_subgraph

Add subgraphs to the graph.](/python/langchain-core/runnables/graph_png/PngDrawer/add_subgraph)[method

add\_edges

Add edges to the graph.](/python/langchain-core/runnables/graph_png/PngDrawer/add_edges)[method

update\_styles

Update the styles of the entrypoint and END nodes.](/python/langchain-core/runnables/graph_png/PngDrawer/update_styles)


