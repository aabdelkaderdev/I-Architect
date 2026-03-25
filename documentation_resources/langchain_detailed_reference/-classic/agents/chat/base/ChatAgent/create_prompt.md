<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/base/ChatAgent/create_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# create\_prompt

Create a prompt from a list of tools.


```
create_prompt(
  cls,
  tools: Sequence[BaseTool],
  system_message_prefix: str = SYSTEM_MESSAGE_PREFIX,
  system_message_suffix: str = SYSTEM_MESSAGE_SUFFIX,
  human_message: str = HUMAN_MESSAGE,
  format_instructions: str = FORMAT_INSTRUCTIONS,
  input_variables: list[str] | None = None
) -> BasePromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `Sequence[BaseTool]` | A list of tools. |
| `system_message_prefix` | `str` | Default:`SYSTEM_MESSAGE_PREFIX`  The system message prefix. |
| `system_message_suffix` | `str` | Default:`SYSTEM_MESSAGE_SUFFIX`  The system message suffix. |
| `human_message` | `str` | Default:`HUMAN_MESSAGE`  The `HumanMessage`. |
| `format_instructions` | `str` | Default:`FORMAT_INSTRUCTIONS`  The format instructions. |
| `input_variables` | `list[str] | None` | Default:`None`  The input variables. |


