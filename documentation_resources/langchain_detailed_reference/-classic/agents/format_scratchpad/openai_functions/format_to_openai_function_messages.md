<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/format_scratchpad/openai_functions/format_to_openai_function_messages -->

Functionv1.2.13 (latest)●Since v1.0

# format\_to\_openai\_function\_messages

Convert (AgentAction, tool output) tuples into FunctionMessages.


```
format_to_openai_function_messages(
  intermediate_steps: Sequence[tuple[AgentAction, str]]
) -> list[BaseMessage]
```

Raises:
ValueError: if the observation cannot be converted to a string.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `Sequence[tuple[AgentAction, str]]` | Steps the LLM has taken to date, along with observations |


