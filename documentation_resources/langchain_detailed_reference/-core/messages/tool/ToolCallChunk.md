<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/ToolCallChunk -->

Classv1.2.21 (latest)●Since v0.1

# ToolCallChunk

A chunk of a tool call (yielded when streaming).

When merging `ToolCallChunk` objects (e.g., via `AIMessageChunk.__add__`), all
string attributes are concatenated. Chunks are only merged if their values of
`index` are equal and not `None`.

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
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| args | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| index | [int](https://docs.python.org/3/library/functions.html#int) | None |
| type | NotRequired[[Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['tool\_call\_chunk']] |

## Attributes

[attribute

name: str | None

The name of the tool to be called.](/python/langchain-core/messages/tool/ToolCallChunk/name)[attribute

args: str | None

The arguments to the tool call as a JSON-parseable string.](/python/langchain-core/messages/tool/ToolCallChunk/args)[attribute

id: str | None

An identifier associated with the tool call.

An identifier is needed to associate a tool call request with a tool
call result in events when multiple concurrent tool calls are made.](/python/langchain-core/messages/tool/ToolCallChunk/id)[attribute

index: int | None

The index of the tool call in a sequence.

Used for merging chunks.](/python/langchain-core/messages/tool/ToolCallChunk/index)[attribute

type: NotRequired[Literal['tool\_call\_chunk']]

Used for discrimination.](/python/langchain-core/messages/tool/ToolCallChunk/type)


