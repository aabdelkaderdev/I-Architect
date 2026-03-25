<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/RejectDecision -->

Classv1.2.13 (latest)●Since v1.0

# RejectDecision

Response when a human rejects the action.


```
RejectDecision()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['reject'] |
| message | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str)] |

## Attributes

[attribute

type: Literal['reject']

The type of response when a human rejects the action.](/python/langchain/agents/middleware/human_in_the_loop/RejectDecision/type)[attribute

message: NotRequired[str]

The message sent to the model explaining why the action was rejected.](/python/langchain/agents/middleware/human_in_the_loop/RejectDecision/message)


