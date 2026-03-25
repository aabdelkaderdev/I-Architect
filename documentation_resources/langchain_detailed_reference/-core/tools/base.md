<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base -->

Modulev1.2.21 (latest)●Since v0.2

# base

Base classes and utilities for LangChain tools.

## Attributes

## Functions

## Classes

## Type Aliases



[attribute

TypeBaseModel: type[BaseModel]](/python/langchain-core/utils/pydantic/TypeBaseModel)

[attribute

FILTERED\_ARGS](/python/langchain-core/tools/base/FILTERED_ARGS)

[attribute

TOOL\_MESSAGE\_BLOCK\_TYPES](/python/langchain-core/tools/base/TOOL_MESSAGE_BLOCK_TYPES)

[function

ensure\_config](/python/langchain-core/runnables/config/ensure_config)

[function

patch\_config](/python/langchain-core/runnables/config/patch_config)

[function

run\_in\_executor](/python/langchain-core/runnables/config/run_in_executor)

[function

set\_config\_context](/python/langchain-core/runnables/config/set_config_context)

[function

coro\_with\_context](/python/langchain-core/runnables/utils/coro_with_context)

[function

get\_fields](/python/langchain-core/utils/pydantic/get_fields)

[function

is\_basemodel\_subclass](/python/langchain-core/utils/pydantic/is_basemodel_subclass)

[function

is\_pydantic\_v1\_subclass](/python/langchain-core/utils/pydantic/is_pydantic_v1_subclass)

[function

is\_pydantic\_v2\_subclass](/python/langchain-core/utils/pydantic/is_pydantic_v2_subclass)

[function

create\_schema\_from\_function](/python/langchain-core/tools/base/create_schema_from_function)

[function

get\_all\_basemodel\_annotations](/python/langchain-core/tools/base/get_all_basemodel_annotations)

[class

AsyncCallbackManager](/python/langchain-core/callbacks/manager/AsyncCallbackManager)

[class

CallbackManager](/python/langchain-core/callbacks/manager/CallbackManager)

[class

ToolCall](/python/langchain-core/messages/tool/ToolCall)

[class

ToolMessage](/python/langchain-core/messages/tool/ToolMessage)

[class

ToolOutputMixin](/python/langchain-core/messages/tool/ToolOutputMixin)

[class

RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig)

[class

RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)

[class

SchemaAnnotationError](/python/langchain-core/tools/base/SchemaAnnotationError)

[class

ToolException](/python/langchain-core/tools/base/ToolException)

[class

BaseTool](/python/langchain-core/tools/base/BaseTool)

[class

InjectedToolArg](/python/langchain-core/tools/base/InjectedToolArg)

[class

InjectedToolCallId](/python/langchain-core/tools/base/InjectedToolCallId)

[class

BaseToolkit](/python/langchain-core/tools/base/BaseToolkit)

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)

[typeAlias

ArgsSchema](/python/langchain-core/tools/base/ArgsSchema)

Ensure that a config is a dict with all keys present.

Patch a config with new values.

Run a function in an executor.

Set the child Runnable config + tracing context.

Await a coroutine with a context.

Return the field names of a Pydantic model.

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x

Check if the given class is Pydantic v1-like.

Check if the given class is Pydantic v2-like.

Create a Pydantic schema from a function's signature.

Get all annotations from a Pydantic `BaseModel` and its parents.

Async callback manager that handles callbacks from LangChain.

Callback manager for LangChain.

Represents an AI's request to call a tool.

Message for passing the result of executing a tool back to a model.

`ToolMessage` objects contain the result of a tool invocation. Typically, the result
is encoded inside the `content` field.

`tool_call_id` is used to associate the tool call request with the tool call
response. Useful in situations where a chat model is able to request multiple tool
calls in parallel.

Mixin for objects that tools can return directly.

If a custom BaseTool is invoked with a `ToolCall` and the output of custom code is
not an instance of `ToolOutputMixin`, the output will automatically be coerced to
a string and wrapped in a `ToolMessage`.

Runnable that can be serialized to JSON.

Raised when `args_schema` is missing or has an incorrect type annotation.

Exception thrown when a tool execution error occurs.

This exception allows tools to signal errors without stopping the agent.

The error is handled according to the tool's `handle_tool_error` setting, and the
result is returned as an observation to the agent.

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.

Annotation for tool arguments that are injected at runtime.

Tool arguments annotated with this class are not included in the tool
schema sent to language models and are instead injected during execution.

Base class for toolkits containing related tools.

A toolkit is a collection of related tools that can be used together to accomplish a
specific task or work with a particular system.

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
```

Annotation for injecting the tool call ID.

This annotation is used to mark a tool parameter that should receive the tool call
ID at runtime.

```
from typing import Annotated
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId

@tool
def foo(
    x: int, tool_call_id: Annotated[str, InjectedToolCallId]
) -> ToolMessage:
    """Return x."""
    return ToolMessage(
        str(x),
        artifact=x,
        name="foo",
        tool_call_id=tool_call_id
    )
```