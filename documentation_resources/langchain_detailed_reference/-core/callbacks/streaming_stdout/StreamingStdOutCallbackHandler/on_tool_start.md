<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/streaming_stdout/StreamingStdOutCallbackHandler/on_tool_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_start

Run when the tool starts running.


```
on_tool_start(
  self,
  serialized: dict[str, Any],
  input_str: str,
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized tool. |
| `input_str`\* | `str` | The input string. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


