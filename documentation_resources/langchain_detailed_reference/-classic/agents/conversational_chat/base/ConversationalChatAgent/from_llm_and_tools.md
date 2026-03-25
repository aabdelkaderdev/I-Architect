<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/conversational_chat/base/ConversationalChatAgent/from_llm_and_tools -->

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
  system_message: str = PREFIX,
  human_message: str = SUFFIX,
  input_variables: list[str] | None = None,
  **kwargs: Any = {}
) -> Agent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `tools`\* | `Sequence[BaseTool]` | A list of tools to use. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  The callback manager to use. |
| `output_parser` | `AgentOutputParser | None` | Default:`None`  The output parser to use. |
| `system_message` | `str` | Default:`PREFIX`  The `SystemMessage` to use. |
| `human_message` | `str` | Default:`SUFFIX`  The `HumanMessage` to use. |
| `input_variables` | `list[str] | None` | Default:`None`  The input variables to use. |
| `**kwargs` | `Any` | Default:`{}`  Any additional arguments. |


