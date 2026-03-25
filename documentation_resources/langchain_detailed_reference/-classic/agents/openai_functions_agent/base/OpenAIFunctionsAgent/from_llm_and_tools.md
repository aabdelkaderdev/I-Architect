<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_functions_agent/base/OpenAIFunctionsAgent/from_llm_and_tools -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm\_and\_tools

Construct an agent from an LLM and tools.


```
from_llm_and_tools(
  cls,
  llm: BaseLanguageModel,
  tools: Sequence[BaseTool],
  callback_manager: BaseCallbackManager | None = None,
  extra_prompt_messages: list[BaseMessagePromptTemplate] | None = None,
  system_message: SystemMessage | None = _NOT_SET,
  **kwargs: Any = {}
) -> BaseSingleActionAgent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use as the agent. |
| `tools`\* | `Sequence[BaseTool]` | The tools to use. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  The callback manager to use. |
| `extra_prompt_messages` | `list[BaseMessagePromptTemplate] | None` | Default:`None`  Extra prompt messages to use. |
| `system_message` | `SystemMessage | None` | Default:`_NOT_SET`  The system message to use. Defaults to a default system message. |
| `kwargs` | `Any` | Default:`{}`  Additional parameters to pass to the agent. |


