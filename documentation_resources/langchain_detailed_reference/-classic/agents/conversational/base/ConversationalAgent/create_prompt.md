<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational/base/ConversationalAgent/create_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# create\_prompt

Create prompt in the style of the zero-shot agent.


```
create_prompt(
  cls,
  tools: Sequence[BaseTool],
  prefix: str = PREFIX,
  suffix: str = SUFFIX,
  format_instructions: str = FORMAT_INSTRUCTIONS,
  ai_prefix: str = 'AI',
  human_prefix: str = 'Human',
  input_variables: list[str] | None = None
) -> PromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `Sequence[BaseTool]` | List of tools the agent will have access to, used to format the prompt. |
| `prefix` | `str` | Default:`PREFIX`  String to put before the list of tools. |
| `suffix` | `str` | Default:`SUFFIX`  String to put after the list of tools. |
| `format_instructions` | `str` | Default:`FORMAT_INSTRUCTIONS`  Instructions on how to use the tools. |
| `ai_prefix` | `str` | Default:`'AI'`  String to use before AI output. |
| `human_prefix` | `str` | Default:`'Human'`  String to use before human output. |
| `input_variables` | `list[str] | None` | Default:`None`  List of input variables the final prompt will expect. Defaults to `["input", "chat_history", "agent_scratchpad"]`. |


