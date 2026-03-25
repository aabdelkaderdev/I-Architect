<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/base/ChatAgent/from_llm_and_tools -->

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
  system_message_prefix: str = SYSTEM_MESSAGE_PREFIX,
  system_message_suffix: str = SYSTEM_MESSAGE_SUFFIX,
  human_message: str = HUMAN_MESSAGE,
  format_instructions: str = FORMAT_INSTRUCTIONS,
  input_variables: list[str] | None = None,
  **kwargs: Any = {}
) -> Agent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model. |
| `tools`\* | `Sequence[BaseTool]` | A list of tools. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  The callback manager. |
| `output_parser` | `AgentOutputParser | None` | Default:`None`  The output parser. |
| `system_message_prefix` | `str` | Default:`SYSTEM_MESSAGE_PREFIX`  The system message prefix. |
| `system_message_suffix` | `str` | Default:`SYSTEM_MESSAGE_SUFFIX`  The system message suffix. |
| `human_message` | `str` | Default:`HUMAN_MESSAGE`  The `HumanMessage`. |
| `format_instructions` | `str` | Default:`FORMAT_INSTRUCTIONS`  The format instructions. |
| `input_variables` | `list[str] | None` | Default:`None`  The input variables. |
| `kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


