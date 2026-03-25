<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig -->

Classv1.2.13 (latest)●Since v1.0

# ReviewConfig

Policy for reviewing a HITL request.


```
ReviewConfig()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| action\_name | [str](https://docs.python.org/3/library/stdtypes.html#str) |
| allowed\_decisions | [list](https://docs.python.org/3/library/stdtypes.html#list)[[DecisionType](/python/langchain/agents/middleware/human_in_the_loop/DecisionType)] |
| args\_schema | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

action\_name: str

Name of the action associated with this review configuration.](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig/action_name)[attribute

allowed\_decisions: list[DecisionType]

The decisions that are allowed for this request.](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig/allowed_decisions)[attribute

args\_schema: NotRequired[dict[str, Any]]

JSON schema for the args associated with the action, if edits are allowed.](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig/args_schema)


