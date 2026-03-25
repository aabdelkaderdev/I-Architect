<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/mrkl/base/ZeroShotAgent/from_llm_and_tools -->

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
  format_instructions: str = FORMAT_INSTRUCTIONS,
  input_variables: list[str] | None = None,
  **kwargs: Any = {}
) -> Agent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use as the agent LLM. |
| `tools`\* | `Sequence[BaseTool]` | The tools to use. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  The callback manager to use. |
| `output_parser` | `AgentOutputParser | None` | Default:`None`  The output parser to use. |
| `prefix` | `str` | Default:`PREFIX`  The prefix to use. |
| `suffix` | `str` | Default:`SUFFIX`  The suffix to use. |
| `format_instructions` | `str` | Default:`FORMAT_INSTRUCTIONS`  The format instructions to use. |
| `input_variables` | `list[str] | None` | Default:`None`  The input variables to use. |
| `kwargs` | `Any` | Default:`{}`  Additional parameters to pass to the agent. |


