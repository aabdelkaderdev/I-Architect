<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/base/StructuredChatAgent/create_prompt -->

Methodv1.2.13 (latest)●Since v1.0

# create\_prompt


```
create_prompt(
  cls,
  tools: Sequence[BaseTool],
  prefix: str = PREFIX,
  suffix: str = SUFFIX,
  human_message_template: str = HUMAN_MESSAGE_TEMPLATE,
  format_instructions: str = FORMAT_INSTRUCTIONS,
  input_variables: list[str] | None = None,
  memory_prompts: list[BasePromptTemplate] | None = None
) -> BasePromptTemplate
```


