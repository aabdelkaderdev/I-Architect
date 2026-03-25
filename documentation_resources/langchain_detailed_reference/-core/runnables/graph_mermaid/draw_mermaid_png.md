<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph_mermaid/draw_mermaid_png -->

Functionv1.2.21 (latest)●Since v0.1

# draw\_mermaid\_png

Draws a Mermaid graph as PNG using provided syntax.


```
draw_mermaid_png(
  mermaid_syntax: str,
  output_file_path: str | None = None,
  draw_method: MermaidDrawMethod = MermaidDrawMethod.API,
  background_color: str | None = 'white',
  padding: int = 10,
  max_retries: int = 1,
  retry_delay: float = 1.0,
  base_url: str | None = None,
  proxies: dict[str, str] | None = None
) -> bytes
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `mermaid_syntax`\* | `str` | Mermaid graph syntax. |
| `output_file_path` | `str | None` | Default:`None`  Path to save the PNG image. |
| `draw_method` | `MermaidDrawMethod` | Default:`MermaidDrawMethod.API`  Method to draw the graph. |
| `background_color` | `str | None` | Default:`'white'`  Background color of the image. |
| `padding` | `int` | Default:`10`  Padding around the image. |
| `max_retries` | `int` | Default:`1`  Maximum number of retries (MermaidDrawMethod.API). |
| `retry_delay` | `float` | Default:`1.0`  Delay between retries (MermaidDrawMethod.API). |
| `base_url` | `str | None` | Default:`None`  Base URL for the Mermaid.ink API. |
| `proxies` | `dict[str, str] | None` | Default:`None`  HTTP/HTTPS proxies for requests (e.g. `{"http": "http://127.0.0.1:7890"}`). |


