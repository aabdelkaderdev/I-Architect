<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/format_scratchpad/log_to_messages/format_log_to_messages -->

Functionv1.2.13 (latest)●Since v1.0

# format\_log\_to\_messages

Construct the scratchpad that lets the agent continue its thought process.


```
format_log_to_messages(
  intermediate_steps: list[tuple[AgentAction, str]],
  template_tool_response: str = '{observation}'
) -> list[BaseMessage]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | List of tuples of AgentAction and observation strings. |
| `template_tool_response` | `str` | Default:`'{observation}'`  Template to format the observation with. Defaults to `"{observation}"`. |


