<!-- Source: https://reference.langchain.com/python/langchain-core/tools/simple -->

Modulev1.2.21 (latest)●Since v0.2

# simple

Tool that takes in function or coroutine directly.

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

AsyncCallbackManagerForToolRun

Async callback manager for tool run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForToolRun)[class

CallbackManagerForToolRun

Callback manager for tool run.](/python/langchain-core/callbacks/manager/CallbackManagerForToolRun)[class

RunnableConfig

Configuration for a `Runnable`.

Note

Custom values

The `TypedDict` has `total=False` set intentionally to:

- Allow partial configs to be created and merged together via `merge_configs`
- Support config propagation from parent to child runnables via
  `var_child_runnable_config` (a `ContextVar` that automatically passes
  config down the call stack without explicit parameter passing), where
  configs are merged rather than replaced

Example

```
# Parent sets tags
chain.invoke(input, config={"tags": ["parent"]})
# Child automatically inherits and can add:
# ensure_config({"tags": ["child"]}) -> {"tags": ["parent", "child"]}
```](/python/langchain-core/runnables/config/RunnableConfig)[class

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)[class

ToolException

Exception thrown when a tool execution error occurs.

This exception allows tools to signal errors without stopping the agent.

The error is handled according to the tool's `handle_tool_error` setting, and the
result is returned as an observation to the agent.](/python/langchain-core/tools/base/ToolException)[class

ToolCall

Represents an AI's request to call a tool.](/python/langchain-core/messages/tool/ToolCall)[class

Tool

Tool that takes in function or coroutine directly.](/python/langchain-core/tools/simple/Tool)

## Type Aliases

[typeAlias

ArgsSchema](/python/langchain-core/tools/base/ArgsSchema)


