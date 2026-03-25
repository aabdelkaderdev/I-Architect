<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_ascii/draw_ascii -->

Functionv1.2.21 (latest)●Since v0.1

# draw\_ascii

Build a DAG and draw it in ASCII.


```
draw_ascii(
    vertices: Mapping[str, str],
    edges: Sequence[LangEdge],
) -> str
```

**Example:**

```
from langchain_core.runnables.graph_ascii import draw_ascii

vertices = {1: "1", 2: "2", 3: "3", 4: "4"}
edges = [
    (source, target, None, None)
    for source, target in [(1, 2), (2, 3), (2, 4), (1, 4)]
]

print(draw_ascii(vertices, edges))
```

```
         +---+
         | 1 |
         +---+
         *    *
        *     *
       *       *
    +---+       *
    | 2 |       *
    +---+**     *
      *    **   *
      *      ** *
      *        **
    +---+     +---+
    | 3 |     | 4 |
    +---+     +---+
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `vertices`\* | `Mapping[str, str]` | list of graph vertices. |
| `edges`\* | `Sequence[LangEdge]` | list of graph edges. |


