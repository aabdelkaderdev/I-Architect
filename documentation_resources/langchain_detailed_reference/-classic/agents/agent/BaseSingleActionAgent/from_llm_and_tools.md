<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/BaseSingleActionAgent/from_llm_and_tools -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm\_and\_tools

Construct an agent from an LLM and tools.


```
from_llm_and_tools(
  cls,
  llm: BaseLanguageModel,
  tools: Sequence[BaseTool],
  callback_manager: BaseCallbackManager | None = None,
  **kwargs: Any = {}
) -> BaseSingleActionAgent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | Language model to use. |
| `tools`\* | `Sequence[BaseTool]` | Tools to use. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  Callback manager to use. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


