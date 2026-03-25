<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph/Graph -->

Classv1.2.21 (latest)●Since v0.1

# Graph

Graph of nodes and edges.


```
Graph(
  self,
  nodes: dict[str, Node] = dict(),
  edges: list[Edge] = list()
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `nodes` | `dict[str, Node]` | Default:`dict()`  Dictionary of nodes in the graph. Defaults to an empty dictionary. |
| `edges` | `list[Edge]` | Default:`list()`  List of edges in the graph. Defaults to an empty list. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| nodes | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Node](/python/langchain-core/runnables/graph/Node)] |
| edges | [list](https://docs.python.org/3/library/stdtypes.html#list)[[Edge](/python/langchain-core/runnables/graph/Edge)] |

## Attributes

[attribute

nodes: dict[str, Node]](/python/langchain-core/runnables/graph/Graph/nodes)[attribute

edges: list[Edge]](/python/langchain-core/runnables/graph/Graph/edges)

## Methods

[method

to\_json

Convert the graph to a JSON-serializable format.](/python/langchain-core/runnables/graph/Graph/to_json)[method

next\_id

Return a new unique node identifier.

It that can be used to add a node to the graph.](/python/langchain-core/runnables/graph/Graph/next_id)[method

add\_node

Add a node to the graph and return it.](/python/langchain-core/runnables/graph/Graph/add_node)[method

remove\_node

Remove a node from the graph and all edges connected to it.](/python/langchain-core/runnables/graph/Graph/remove_node)[method

add\_edge

Add an edge to the graph and return it.](/python/langchain-core/runnables/graph/Graph/add_edge)[method

extend

Add all nodes and edges from another graph.

Note this doesn't check for duplicates, nor does it connect the graphs.](/python/langchain-core/runnables/graph/Graph/extend)[method

reid

Return a new graph with all nodes re-identified.

Uses their unique, readable names where possible.](/python/langchain-core/runnables/graph/Graph/reid)[method

first\_node

Find the single node that is not a target of any edge.

If there is no such node, or there are multiple, return `None`.
When drawing the graph, this node would be the origin.](/python/langchain-core/runnables/graph/Graph/first_node)[method

last\_node

Find the single node that is not a source of any edge.

If there is no such node, or there are multiple, return `None`.
When drawing the graph, this node would be the destination.](/python/langchain-core/runnables/graph/Graph/last_node)[method

trim\_first\_node

Remove the first node if it exists and has a single outgoing edge.

i.e., if removing it would not leave the graph without a "first" node.](/python/langchain-core/runnables/graph/Graph/trim_first_node)[method

trim\_last\_node

Remove the last node if it exists and has a single incoming edge.

i.e., if removing it would not leave the graph without a "last" node.](/python/langchain-core/runnables/graph/Graph/trim_last_node)[method

draw\_ascii

Draw the graph as an ASCII art string.](/python/langchain-core/runnables/graph/Graph/draw_ascii)[method

print\_ascii

Print the graph as an ASCII art string.](/python/langchain-core/runnables/graph/Graph/print_ascii)[method

draw\_png

Draw the graph as a PNG image.](/python/langchain-core/runnables/graph/Graph/draw_png)[method

draw\_mermaid

Draw the graph as a Mermaid syntax string.](/python/langchain-core/runnables/graph/Graph/draw_mermaid)[method

draw\_mermaid\_png

Draw the graph as a PNG image using Mermaid.](/python/langchain-core/runnables/graph/Graph/draw_mermaid_png)


