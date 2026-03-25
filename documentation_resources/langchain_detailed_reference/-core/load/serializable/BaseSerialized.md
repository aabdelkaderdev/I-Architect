<!-- Source: https://reference.langchain.com/python/langchain-core/load/serializable/BaseSerialized -->

Classv1.2.21 (latest)●Since v0.1

# BaseSerialized

Base class for serialized objects.


```
BaseSerialized()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| lc | [int](https://docs.python.org/3/library/functions.html#int) |
| id | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| name | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str)] |
| graph | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

lc: int

The version of the serialization format.](/python/langchain-core/load/serializable/BaseSerialized/lc)[attribute

id: list[str]

The unique identifier of the object.](/python/langchain-core/load/serializable/BaseSerialized/id)[attribute

name: NotRequired[str]

The name of the object.](/python/langchain-core/load/serializable/BaseSerialized/name)[attribute

graph: NotRequired[dict[str, Any]]

The graph of the object.](/python/langchain-core/load/serializable/BaseSerialized/graph)


