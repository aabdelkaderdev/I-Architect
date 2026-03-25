<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/loading/load_agent_from_config -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# load\_agent\_from\_config

Load agent from Config Dict.


```
load_agent_from_config(
  config: dict,
  llm: BaseLanguageModel | None = None,
  tools: list[Tool] | None = None,
  **kwargs: Any = {}
) -> BaseSingleActionAgent | BaseMultiActionAgent
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config`\* | `dict` | Config dict to load agent from. |
| `llm` | `BaseLanguageModel | None` | Default:`None`  Language model to use as the agent. |
| `tools` | `list[Tool] | None` | Default:`None`  List of tools this agent has access to. |
| `kwargs` | `Any` | Default:`{}`  Additional keyword arguments passed to the agent executor. |


