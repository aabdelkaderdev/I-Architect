<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/ToolCallChunk -->

Classv1.2.21 (latest)●Since v1.0

# ToolCallChunk

A chunk of a tool call (yielded when streaming).

When merging `ToolCallChunks` (e.g., via `AIMessageChunk.__add__`),
all string attributes are concatenated. Chunks are only merged if their
values of `index` are equal and not `None`.

Example:

```
left_chunks = [ToolCallChunk(name="foo", args='{"a":', index=0)]
right_chunks = [ToolCallChunk(name=None, args="1}", index=0)]

(
    AIMessageChunk(content="", tool_call_chunks=left_chunks)
    + AIMessageChunk(content="", tool_call_chunks=right_chunks)
).tool_call_chunks == [ToolCallChunk(name="foo", args='{"a":1}', index=0)]
```


```
ToolCallChunk()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['tool\_call\_chunk'] |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| args | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| index | NotRequired[[int](https://docs.python.org/3/library/functions.html#int) | [str](https://docs.python.org/3/library/stdtypes.html#str)] |
| extras | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

type: Literal['tool\_call\_chunk']

Used for serialization.](/python/langchain-core/messages/content/ToolCallChunk/type)[attribute

id: str | None

An identifier associated with the tool call.

An identifier is needed to associate a tool call request with a tool
call result in events when multiple concurrent tool calls are made.](/python/langchain-core/messages/content/ToolCallChunk/id)[attribute

name: str | None

The name of the tool to be called.](/python/langchain-core/messages/content/ToolCallChunk/name)[attribute

args: str | None

The arguments to the tool call.](/python/langchain-core/messages/content/ToolCallChunk/args)[attribute

index: NotRequired[int | str]

The index of the tool call in a sequence.](/python/langchain-core/messages/content/ToolCallChunk/index)[attribute

extras: NotRequired[dict[str, Any]]

Provider-specific metadata.](/python/langchain-core/messages/content/ToolCallChunk/extras)


