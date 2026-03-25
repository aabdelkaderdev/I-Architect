<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/create_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# create\_prompt

Create a prompt for the agent.


```
create_prompt(
  cls,
  tools: Sequence[BaseTool],
  system_message: str = PREFIX,
  human_message: str = SUFFIX,
  input_variables: list[str] | None = None,
  output_parser: BaseOutputParser | None = None
) -> BasePromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `Sequence[BaseTool]` | The tools to use. |
| `system_message` | `str` | Default:`PREFIX`  The `SystemMessage` to use. |
| `human_message` | `str` | Default:`SUFFIX`  The `HumanMessage` to use. |
| `input_variables` | `list[str] | None` | Default:`None`  The input variables to use. |
| `output_parser` | `BaseOutputParser | None` | Default:`None`  The output parser to use. |


