<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/initialize/initialize_agent -->

Functionv1.2.13 (latest)●Since v1.0Deprecated

# initialize\_agent

Load an agent executor given tools and LLM.

Warning

This function is no deprecated in favor of
[`create_agent`](/python/langchain/agents/create_agent) from the `langchain`
package, which provides a more flexible agent factory with middleware
support, structured output, and integration with LangGraph.

For migration guidance, see
[Migrating to langchain v1](https://docs.langchain.com/oss/python/migrate/langchain-v1)
and
[Migrating from AgentExecutor](https://python.langchain.com/docs/how_to/migrate_agent/).


```
initialize_agent(
  tools: Sequence[BaseTool],
  llm: BaseLanguageModel,
  agent: AgentType | None = None,
  callback_manager: BaseCallbackManager | None = None,
  agent_path: str | None = None,
  agent_kwargs: dict | None = None,
  *,
  tags: Sequence[str] | None = None,
  **kwargs: Any = {}
) -> AgentExecutor
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `Sequence[BaseTool]` | List of tools this agent has access to. |
| `llm`\* | `BaseLanguageModel` | Language model to use as the agent. |
| `agent` | `AgentType | None` | Default:`None`  Agent type to use. If `None` and agent\_path is also None, will default to AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION. |
| `callback_manager` | `BaseCallbackManager | None` | Default:`None`  CallbackManager to use. Global callback manager is used if not provided. |
| `agent_path` | `str | None` | Default:`None`  Path to serialized agent to use. If `None` and agent is also None, will default to AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION. |
| `agent_kwargs` | `dict | None` | Default:`None`  Additional keyword arguments to pass to the underlying agent. |
| `tags` | `Sequence[str] | None` | Default:`None`  Tags to apply to the traced runs. |
| `kwargs` | `Any` | Default:`{}`  Additional keyword arguments passed to the agent executor. |


