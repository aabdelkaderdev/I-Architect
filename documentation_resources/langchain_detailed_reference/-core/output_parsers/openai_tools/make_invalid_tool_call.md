<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_tools/make_invalid_tool_call -->

Functionv1.2.21 (latest)●Since v0.1

# make\_invalid\_tool\_call

Create an `InvalidToolCall` from a raw tool call.


```
make_invalid_tool_call(
  raw_tool_call: dict[str, Any],
  error_msg: str | None
) -> InvalidToolCall
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_tool_call`\* | `dict[str, Any]` | The raw tool call. |
| `error_msg`\* | `str | None` | The error message. |


