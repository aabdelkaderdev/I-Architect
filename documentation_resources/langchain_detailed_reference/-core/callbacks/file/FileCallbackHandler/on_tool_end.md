<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler/on_tool_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_end

Handle tool end by writing the output with optional prefixes.


```
on_tool_end(
  self,
  output: str,
  color: str | None = None,
  observation_prefix: str | None = None,
  llm_prefix: str | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `output`\* | `str` | The tool output to write. |
| `color` | `str | None` | Default:`None`  Color override for this specific output.  If `None`, uses `self.color`. |
| `observation_prefix` | `str | None` | Default:`None`  Optional prefix to write before the output. |
| `llm_prefix` | `str | None` | Default:`None`  Optional prefix to write after the output. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


