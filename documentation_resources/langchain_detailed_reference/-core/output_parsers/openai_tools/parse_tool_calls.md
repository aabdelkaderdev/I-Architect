<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_tools/parse_tool_calls -->

Functionv1.2.21 (latest)●Since v0.1

# parse\_tool\_calls

Parse a list of tool calls.


```
parse_tool_calls(
  raw_tool_calls: list[dict],
  *,
  partial: bool = False,
  strict: bool = False,
  return_id: bool = True
) -> list[dict[str, Any]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_tool_calls`\* | `list[dict]` | The raw tool calls to parse. |
| `partial` | `bool` | Default:`False`  Whether to parse partial JSON. |
| `strict` | `bool` | Default:`False`  Whether to allow non-JSON-compliant strings. |
| `return_id` | `bool` | Default:`True`  Whether to return the tool call id. |


