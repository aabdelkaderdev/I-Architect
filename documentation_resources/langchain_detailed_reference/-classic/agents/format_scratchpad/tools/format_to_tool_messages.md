<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/format_scratchpad/tools/format_to_tool_messages -->

Functionv1.2.13 (latest)●Since v1.0

# format\_to\_tool\_messages

Convert (AgentAction, tool output) tuples into `ToolMessage` objects.


```
format_to_tool_messages(
  intermediate_steps: Sequence[tuple[AgentAction, str]]
) -> list[BaseMessage]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `Sequence[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations. |


