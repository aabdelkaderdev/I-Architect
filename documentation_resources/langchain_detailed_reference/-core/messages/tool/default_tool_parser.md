<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/default_tool_parser -->

Functionv1.2.21 (latest)●Since v0.1

# default\_tool\_parser

Best-effort parsing of tools.


```
default_tool_parser(
  raw_tool_calls: list[dict]
) -> tuple[list[ToolCall], list[InvalidToolCall]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `raw_tool_calls`\* | `list[dict]` | List of raw tool call dicts to parse. |


