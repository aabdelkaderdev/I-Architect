<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/Action -->

Classv1.2.13 (latest)●Since v1.0

# Action

Represents an action with a name and args.


```
Action()
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

## Attributes

[attribute

name: str

The type or name of action being requested (e.g., `'add_numbers'`).](/python/langchain/agents/middleware/human_in_the_loop/Action/name)[attribute

args: dict[str, Any]

Key-value pairs of args needed for the action (e.g., `{"a": 1, "b": 2}`).](/python/langchain/agents/middleware/human_in_the_loop/Action/args)


