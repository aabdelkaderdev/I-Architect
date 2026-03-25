<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/InvalidToolCall -->

Classv1.2.21 (latest)●Since v1.0

# InvalidToolCall

Allowance for errors made by LLM.

Here we add an `error` key to surface errors made during generation
(e.g., invalid JSON arguments.)


```
InvalidToolCall()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['invalid\_tool\_call'] |
| id | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| args | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| error | [str](https://docs.python.org/3/library/stdtypes.html#str) | None |
| index | NotRequired[[int](https://docs.python.org/3/library/functions.html#int) | [str](https://docs.python.org/3/library/stdtypes.html#str)] |
| extras | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

type: Literal['invalid\_tool\_call']

Used for discrimination.](/python/langchain-core/messages/content/InvalidToolCall/type)[attribute

id: str | None

An identifier associated with the tool call.

An identifier is needed to associate a tool call request with a tool
call result in events when multiple concurrent tool calls are made.](/python/langchain-core/messages/content/InvalidToolCall/id)[attribute

name: str | None

The name of the tool to be called.](/python/langchain-core/messages/content/InvalidToolCall/name)[attribute

args: str | None

The arguments to the tool call.](/python/langchain-core/messages/content/InvalidToolCall/args)[attribute

error: str | None

An error message associated with the tool call.](/python/langchain-core/messages/content/InvalidToolCall/error)[attribute

index: NotRequired[int | str]

Index of block in aggregate response. Used during streaming.](/python/langchain-core/messages/content/InvalidToolCall/index)[attribute

extras: NotRequired[dict[str, Any]]

Provider-specific metadata.](/python/langchain-core/messages/content/InvalidToolCall/extras)


