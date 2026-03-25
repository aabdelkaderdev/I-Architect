<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/openai_tools/JsonOutputToolsParser/first_tool_only -->

Attributev1.2.21 (latest)●Since v0.1

# first\_tool\_only

Whether to return only the first tool call.

If `False`, the result will be a list of tool calls, or an empty list if no tool
calls are found.

If `True`, and multiple tool calls are found, only the first one will be returned,
and the other tool calls will be ignored.

If no tool calls are found, `None` will be returned.


```
first_tool_only: bool = False
```


