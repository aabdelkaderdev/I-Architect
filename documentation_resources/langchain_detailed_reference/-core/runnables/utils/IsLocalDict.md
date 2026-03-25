<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils/IsLocalDict -->

Classv1.2.21 (latest)●Since v0.1

# IsLocalDict

Check if a name is a local dict.


```
IsLocalDict(
    self,
    name: str,
    keys: set[str],
)
```

## Bases

`ast.NodeVisitor`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name to check. |
| `keys`\* | `set[str]` | The keys to populate. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| keys | [set](https://docs.python.org/3/library/stdtypes.html#set)[[str](https://docs.python.org/3/library/stdtypes.html#str)] |

## Attributes

[attribute

name: name](/python/langchain-core/runnables/utils/IsLocalDict/name)[attribute

keys: keys](/python/langchain-core/runnables/utils/IsLocalDict/keys)

## Methods

[method

visit\_Subscript

Visit a subscript node.](/python/langchain-core/runnables/utils/IsLocalDict/visit_Subscript)[method

visit\_Call

Visit a call node.](/python/langchain-core/runnables/utils/IsLocalDict/visit_Call)


