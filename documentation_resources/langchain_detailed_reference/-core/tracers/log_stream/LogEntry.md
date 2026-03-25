<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/LogEntry -->

Classv1.2.21 (latest)●Since v0.1

# LogEntry

A single entry in the run log.


```
LogEntry()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| type | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| start\_time | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| streamed\_output\_str | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| streamed\_output | [list](https://docs.python.org/3/library/stdtypes.html#list)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| inputs | NotRequired[[Any](https://docs.python.org/3/library/typing.html#typing.Any) | None] |
| final\_output | [Any](https://docs.python.org/3/library/typing.html#typing.Any) | None |
| end\_time | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |

## Attributes

[attribute

id: str

ID of the sub-run.](/python/langchain-core/tracers/log_stream/LogEntry/id)[attribute

name: str

Name of the object being run.](/python/langchain-core/tracers/log_stream/LogEntry/name)[attribute

type: str

Type of the object being run, eg. prompt, chain, llm, etc.](/python/langchain-core/tracers/log_stream/LogEntry/type)[attribute

tags: list[str]

List of tags for the run.](/python/langchain-core/tracers/log_stream/LogEntry/tags)[attribute

metadata: dict[str, Any]

Key-value pairs of metadata for the run.](/python/langchain-core/tracers/log_stream/LogEntry/metadata)[attribute

start\_time: str

ISO-8601 timestamp of when the run started.](/python/langchain-core/tracers/log_stream/LogEntry/start_time)[attribute

streamed\_output\_str: list[str]

List of LLM tokens streamed by this run, if applicable.](/python/langchain-core/tracers/log_stream/LogEntry/streamed_output_str)[attribute

streamed\_output: list[Any]

List of output chunks streamed by this run, if available.](/python/langchain-core/tracers/log_stream/LogEntry/streamed_output)[attribute

inputs: NotRequired[Any | None]

Inputs to this run. Not available currently via `astream_log`.](/python/langchain-core/tracers/log_stream/LogEntry/inputs)[attribute

final\_output: Any | None

Final output of this run.

Only available after the run has finished successfully.](/python/langchain-core/tracers/log_stream/LogEntry/final_output)[attribute

end\_time: str | None

ISO-8601 timestamp of when the run ended.

Only available after the run has finished.](/python/langchain-core/tracers/log_stream/LogEntry/end_time)


