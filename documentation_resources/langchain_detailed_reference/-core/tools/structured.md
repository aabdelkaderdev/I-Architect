<!-- Source: https://reference.langchain.com/python/langchain-core/tools/structured -->

Modulev1.2.21 (latest)●Since v0.2

# structured

Structured tool.

## Attributes

[attribute

FILTERED\_ARGS](/python/langchain-core/tools/base/FILTERED_ARGS)

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)[function

create\_schema\_from\_function

Create a Pydantic schema from a function's signature.](/python/langchain-core/tools/base/create_schema_from_function)[function

is\_basemodel\_subclass

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x](/python/langchain-core/utils/pydantic/is_basemodel_subclass)

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

ToolCall

Represents an AI's request to call a tool.](/python/langchain-core/messages/tool/ToolCall)[class

StructuredTool

Tool that can operate on any number of inputs.](/python/langchain-core/tools/structured/StructuredTool)

## Type Aliases

[typeAlias

ArgsSchema](/python/langchain-core/tools/base/ArgsSchema)


