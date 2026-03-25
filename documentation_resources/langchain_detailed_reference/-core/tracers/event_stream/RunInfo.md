<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/event_stream/RunInfo -->

Classv1.2.21 (latest)●Since v0.2

# RunInfo

Information about a run.

This is used to keep track of the metadata associated with a run.


```
RunInfo()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| run\_type | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| inputs | NotRequired[[Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| parent\_run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) | None |
| tool\_call\_id | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str) | None] |

## Attributes

[attribute

name: str

The name of the run.](/python/langchain-core/tracers/event_stream/RunInfo/name)[attribute

tags: list[str]

The tags associated with the run.](/python/langchain-core/tracers/event_stream/RunInfo/tags)[attribute

metadata: dict[str, Any]

The metadata associated with the run.](/python/langchain-core/tracers/event_stream/RunInfo/metadata)[attribute

run\_type: str

The type of the run.](/python/langchain-core/tracers/event_stream/RunInfo/run_type)[attribute

inputs: NotRequired[Any]

The inputs to the run.](/python/langchain-core/tracers/event_stream/RunInfo/inputs)[attribute

parent\_run\_id: UUID | None

The ID of the parent run.](/python/langchain-core/tracers/event_stream/RunInfo/parent_run_id)[attribute

tool\_call\_id: NotRequired[str | None]

The tool call ID associated with the run.](/python/langchain-core/tracers/event_stream/RunInfo/tool_call_id)


