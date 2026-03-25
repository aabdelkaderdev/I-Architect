<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_ascii/AsciiCanvas/point -->

Methodv1.2.21 (latest)●Since v0.1

# point

Create a point on ASCII canvas.


```
point(
    self,
    x: int,
    y: int,
    char: str,
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `x`\* | `int` | x coordinate. Should be `>= 0` and `<` number of columns in the canvas. |
| `y`\* | `int` | y coordinate. Should be `>= 0` an `<` number of lines in the canvas. |
| `char`\* | `str` | character to place in the specified point on the canvas. |


