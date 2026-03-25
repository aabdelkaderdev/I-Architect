<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/EventData -->

Classv1.2.21 (latest)●Since v0.1

# EventData

Data associated with a streaming event.


```
EventData()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| input | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |
| error | NotRequired[[BaseException](https://docs.python.org/3/library/exceptions.html#BaseException)] |
| output | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |
| chunk | [Any](https://docs.python.org/3/library/typing.html#typing.Any) |
| tool\_call\_id | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str) | None] |

## Attributes

[attribute

input: Any

The input passed to the `Runnable` that generated the event.

Inputs will sometimes be available at the *START* of the `Runnable`, and
sometimes at the *END* of the `Runnable`.

If a `Runnable` is able to stream its inputs, then its input by definition
won't be known until the *END* of the `Runnable` when it has finished streaming
its inputs.](/python/langchain-core/runnables/schema/EventData/input)[attribute

error: NotRequired[BaseException]

The error that occurred during the execution of the `Runnable`.

This field is only available if the `Runnable` raised an exception.](/python/langchain-core/runnables/schema/EventData/error)[attribute

output: Any

The output of the `Runnable` that generated the event.

Outputs will only be available at the *END* of the `Runnable`.

For most `Runnable` objects, this field can be inferred from the `chunk` field,
though there might be some exceptions for special a cased `Runnable` (e.g., like
chat models), which may return more information.](/python/langchain-core/runnables/schema/EventData/output)[attribute

chunk: Any

A streaming chunk from the output that generated the event.

chunks support addition in general, and adding them up should result
in the output of the `Runnable` that generated the event.](/python/langchain-core/runnables/schema/EventData/chunk)[attribute

tool\_call\_id: NotRequired[str | None]

The tool call ID associated with the tool execution.

This field is available for the `on_tool_error` event and can be used to
link errors to specific tool calls in stateless agent implementations.](/python/langchain-core/runnables/schema/EventData/tool_call_id)


