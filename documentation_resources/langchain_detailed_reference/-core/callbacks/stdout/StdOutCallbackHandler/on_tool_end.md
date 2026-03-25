<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/stdout/StdOutCallbackHandler/on_tool_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_end

If not the final action, print out observation.


```
on_tool_end(
  self,
  output: Any,
  color: str | None = None,
  observation_prefix: str | None = None,
  llm_prefix: str | None = None,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `output`\* | `Any` | The output to print. |
| `color` | `str | None` | Default:`None`  The color to use for the text. |
| `observation_prefix` | `str | None` | Default:`None`  The observation prefix. |
| `llm_prefix` | `str | None` | Default:`None`  The LLM prefix. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


