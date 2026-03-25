<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_tools/parse_tool_call -->

Functionv1.2.21 (latest)●Since v0.1

# parse\_tool\_call

Parse a single tool call.


```
parse_tool_call(
  raw_tool_call: dict[str, Any],
  *,
  partial: bool = False,
  strict: bool = False,
  return_id: bool = True
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_tool_call`\* | `dict[str, Any]` | The raw tool call to parse. |
| `partial` | `bool` | Default:`False`  Whether to parse partial JSON. |
| `strict` | `bool` | Default:`False`  Whether to allow non-JSON-compliant strings. |
| `return_id` | `bool` | Default:`True`  Whether to return the tool call id. |


