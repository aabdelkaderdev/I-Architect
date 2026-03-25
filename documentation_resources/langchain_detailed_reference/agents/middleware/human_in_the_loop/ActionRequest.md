<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/ActionRequest -->

Classv1.2.13 (latest)●Since v0.3

# ActionRequest

Represents an action request with a name, args, and description.


```
ActionRequest()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| args | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] |
| description | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str)] |

## Attributes

[attribute

name: str

The name of the action being requested.](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest/name)[attribute

args: dict[str, Any]

Key-value pairs of args needed for the action (e.g., `{"a": 1, "b": 2}`).](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest/args)[attribute

description: NotRequired[str]

The description of the action to be reviewed.](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest/description)


