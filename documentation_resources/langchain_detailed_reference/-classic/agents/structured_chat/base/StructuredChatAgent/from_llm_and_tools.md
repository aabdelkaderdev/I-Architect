<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/base/StructuredChatAgent/from_llm_and_tools -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm\_and\_tools

Construct an agent from an LLM and tools.


```
from_llm_and_tools(
  cls,
  llm: BaseLanguageModel,
  tools: Sequence[BaseTool],
  callback_manager: BaseCallbackManager | None = None,
  output_parser: AgentOutputParser | None = None,
  prefix: str = PREFIX,
  suffix: str = SUFFIX,
  human_message_template: str = HUMAN_MESSAGE_TEMPLATE,
  format_instructions: str = FORMAT_INSTRUCTIONS,
  input_variables: list[str] | None = None,
  memory_prompts: list[BasePromptTemplate] | None = None,
  **kwargs: Any = {}
) -> Agent
```


