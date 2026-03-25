<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/mrkl/base/MRKLChain/from_chains -->

Methodv1.2.13 (latest)●Since v1.0

# from\_chains

User-friendly way to initialize the MRKL chain.

This is intended to be an easy way to get up and running with the
MRKL chain.


```
from_chains(
  cls,
  llm: BaseLanguageModel,
  chains: list[ChainConfig],
  **kwargs: Any = {}
) -> AgentExecutor
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The LLM to use as the agent LLM. |
| `chains`\* | `list[ChainConfig]` | The chains the MRKL system has access to. |
| `**kwargs` | `Any` | Default:`{}`  parameters to be passed to initialization. |


