<!-- Source: https://reference.langchain.com/python/langchain-core/tools -->

Modulev1.2.21 (latest)●Since v0.1

# tools

Tools are classes that an Agent uses to interact with the world.

Each tool has a description. Agent uses the description to choose the righ tool for the
job.

## Attributes

[attribute

FILTERED\_ARGS](/python/langchain-core/tools/base/FILTERED_ARGS)[attribute

ToolsRenderer: Callable[[list[BaseTool]], str]](/python/langchain-core/tools/render/ToolsRenderer)

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)[function

create\_schema\_from\_function

Create a Pydantic schema from a function's signature.](/python/langchain-core/tools/base/create_schema_from_function)[function

convert\_runnable\_to\_tool

Convert a `Runnable` into a `BaseTool`.](/python/langchain-core/tools/convert/convert_runnable_to_tool)[function

tool

Convert Python functions and `Runnables` to LangChain tools.

Can be used as a decorator with or without arguments to create tools from functions.

Functions can have any signature - the tool will automatically infer input schemas
unless disabled.

Requirements

- Functions should have type hints for proper schema inference.
- Functions may accept multiple arguments and return types are flexible;
  outputs will be serialized if needed.
- When using with `Runnable`, a string name must be provided.](/python/langchain-core/tools/convert/tool)[function

render\_text\_description

Render the tool name and description in plain text.](/python/langchain-core/tools/render/render_text_description)[function

render\_text\_description\_and\_args

Render the tool name, description, and args in plain text.](/python/langchain-core/tools/render/render_text_description_and_args)[function

create\_retriever\_tool

Create a tool to do retrieval of documents.](/python/langchain-core/tools/retriever/create_retriever_tool)

## Classes

[class

BaseTool

Base class for all LangChain tools.

This abstract class defines the interface that all LangChain tools must implement.

Tools are components that can be called by agents to perform specific actions.](/python/langchain-core/tools/base/BaseTool)[class

BaseToolkit

Base class for toolkits containing related tools.

A toolkit is a collection of related tools that can be used together to accomplish a
specific task or work with a particular system.](/python/langchain-core/tools/base/BaseToolkit)[class

InjectedToolArg

Annotation for tool arguments that are injected at runtime.

Tool arguments annotated with this class are not included in the tool
schema sent to language models and are instead injected during execution.](/python/langchain-core/tools/base/InjectedToolArg)[class

InjectedToolCallId

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
```](/python/langchain-core/tools/base/InjectedToolCallId)[class

SchemaAnnotationError

Raised when `args_schema` is missing or has an incorrect type annotation.](/python/langchain-core/tools/base/SchemaAnnotationError)[class

ToolException

Exception thrown when a tool execution error occurs.

This exception allows tools to signal errors without stopping the agent.

The error is handled according to the tool's `handle_tool_error` setting, and the
result is returned as an observation to the agent.](/python/langchain-core/tools/base/ToolException)[class

RetrieverInput

Input to the retriever.](/python/langchain-core/tools/retriever/RetrieverInput)[class

Tool

Tool that takes in function or coroutine directly.](/python/langchain-core/tools/simple/Tool)[class

StructuredTool

Tool that can operate on any number of inputs.](/python/langchain-core/tools/structured/StructuredTool)

## Type Aliases

[typeAlias

ArgsSchema](/python/langchain-core/tools/base/ArgsSchema)

## Modules

[module

base

Base classes and utilities for LangChain tools.](/python/langchain-core/tools/base)[module

simple

Tool that takes in function or coroutine directly.](/python/langchain-core/tools/simple)[module

convert

Convert functions and runnables to tools.](/python/langchain-core/tools/convert)[module

render

Utilities to render tools.](/python/langchain-core/tools/render)[module

structured

Structured tool.](/python/langchain-core/tools/structured)[module

retriever

Retriever tool.](/python/langchain-core/tools/retriever)


