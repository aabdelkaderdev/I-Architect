<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/RunState -->

Classv1.2.21 (latest)●Since v0.1

# RunState

State of the run.


```
RunState()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| streamed\_output | [list](https://docs.python.org/3/library/stdtypes.html#list)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| final\_output | [Any](https://docs.python.org/3/library/typing.html#typing.Any) | None |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| type | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| logs | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [LogEntry](/python/langchain-core/tracers/log_stream/LogEntry)] |

## Attributes

[attribute

id: str

ID of the run.](/python/langchain-core/tracers/log_stream/RunState/id)[attribute

streamed\_output: list[Any]

List of output chunks streamed by `Runnable.stream()`](/python/langchain-core/tracers/log_stream/RunState/streamed_output)[attribute

final\_output: Any | None

Final output of the run, usually the result of aggregating (`+`) streamed\_output.

Updated throughout the run when supported by the `Runnable`.](/python/langchain-core/tracers/log_stream/RunState/final_output)[attribute

name: str

Name of the object being run.](/python/langchain-core/tracers/log_stream/RunState/name)[attribute

type: str

Type of the object being run, e.g. prompt, chain, llm, etc.](/python/langchain-core/tracers/log_stream/RunState/type)[attribute

logs: dict[str, LogEntry]

Map of run names to sub-runs.

If filters were supplied, this list will contain only the runs that matched the
filters.](/python/langchain-core/tracers/log_stream/RunState/logs)


