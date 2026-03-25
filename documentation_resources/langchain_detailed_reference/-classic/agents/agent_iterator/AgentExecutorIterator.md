<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator -->

Classv1.2.13 (latest)●Since v1.0

# AgentExecutorIterator

Iterator for AgentExecutor.


```
AgentExecutorIterator(
  self,
  agent_executor: AgentExecutor,
  inputs: Any,
  callbacks: Callbacks = None,
  *,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  run_name: str | None = None,
  run_id: UUID | None = None,
  include_run_info: bool = False,
  yield_actions: bool = False
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `agent_executor`\* | `AgentExecutor` | The `AgentExecutor` to iterate over. |
| `inputs`\* | `Any` | The inputs to the `AgentExecutor`. |
| `callbacks` | `Callbacks` | Default:`None`  The callbacks to use during iteration. |
| `tags` | `list[str] | None` | Default:`None`  The tags to use during iteration. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata to use during iteration. |
| `run_name` | `str | None` | Default:`None`  The name of the run. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `include_run_info` | `bool` | Default:`False`  Whether to include run info in the output. |
| `yield_actions` | `bool` | Default:`False`  Whether to yield actions as they are generated. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| agent\_executor | [AgentExecutor](/python/langchain-classic/agents/agent/AgentExecutor) |
| inputs | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |
| callbacks | [Callbacks](/python/langchain-mcp-adapters/callbacks/Callbacks) |
| tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |
| run\_name | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) | None |
| include\_run\_info | [bool](https://docs.python.org/3/library/functions.html#bool) |
| yield\_actions | [bool](https://docs.python.org/3/library/functions.html#bool) |

## Attributes

[attribute

inputs: dict[str, str]

The inputs to the `AgentExecutor`.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/inputs)[attribute

callbacks: Callbacks](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/callbacks)[attribute

tags: list[str] | None](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/tags)[attribute

metadata: dict[str, Any] | None](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/metadata)[attribute

run\_name: str | None](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/run_name)[attribute

run\_id: UUID | None](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/run_id)[attribute

include\_run\_info: bool](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/include_run_info)[attribute

yield\_actions: bool](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/yield_actions)[attribute

agent\_executor: AgentExecutor

The `AgentExecutor` to iterate over.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/agent_executor)[attribute

name\_to\_tool\_map: dict[str, BaseTool]

A mapping of tool names to tools.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/name_to_tool_map)[attribute

color\_mapping: dict[str, str]

A mapping of tool names to colors.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/color_mapping)

## Methods

[method

reset

Reset the iterator to its initial state.

Reset the iterator to its initial state, clearing intermediate steps,
iterations, and time elapsed.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/reset)[method

update\_iterations

Increment the number of iterations and update the time elapsed.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/update_iterations)[method

make\_final\_outputs

Make final outputs for the iterator.](/python/langchain-classic/agents/agent_iterator/AgentExecutorIterator/make_final_outputs)


