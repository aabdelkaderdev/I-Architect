<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/EditDecision -->

Classv1.2.13 (latest)●Since v1.0

# EditDecision

Response when a human edits the action.


```
EditDecision()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| type | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['edit'] |
| edited\_action | [Action](/python/langchain/agents/middleware/human_in_the_loop/Action) |

## Attributes

[attribute

type: Literal['edit']

The type of response when a human edits the action.](/python/langchain/agents/middleware/human_in_the_loop/EditDecision/type)[attribute

edited\_action: Action

Edited action for the agent to perform.

Ex: for a tool call, a human reviewer can edit the tool name and args.](/python/langchain/agents/middleware/human_in_the_loop/EditDecision/edited_action)


