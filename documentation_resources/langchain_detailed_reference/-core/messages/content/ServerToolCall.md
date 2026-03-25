<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/ServerToolCall -->

Classv1.2.21 (latest)●Since v1.0

# ServerToolCall

Tool call that is executed server-side.

For example: code execution, web search, etc.


```
ServerToolCall()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['server\_tool\_call'] |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| args | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| index | NotRequired[[int](https://docs.python.org/3/library/functions.html#int) | [str](https://docs.python.org/3/library/stdtypes.html#str)] |
| extras | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

type: Literal['server\_tool\_call']

Used for discrimination.](/python/langchain-core/messages/content/ServerToolCall/type)[attribute

id: str

An identifier associated with the tool call.](/python/langchain-core/messages/content/ServerToolCall/id)[attribute

name: str

The name of the tool to be called.](/python/langchain-core/messages/content/ServerToolCall/name)[attribute

args: dict[str, Any]

The arguments to the tool call.](/python/langchain-core/messages/content/ServerToolCall/args)[attribute

index: NotRequired[int | str]

Index of block in aggregate response. Used during streaming.](/python/langchain-core/messages/content/ServerToolCall/index)[attribute

extras: NotRequired[dict[str, Any]]

Provider-specific metadata.](/python/langchain-core/messages/content/ServerToolCall/extras)


