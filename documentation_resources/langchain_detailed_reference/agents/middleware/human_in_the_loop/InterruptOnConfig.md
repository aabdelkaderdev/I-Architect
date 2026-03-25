<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig -->

Classv1.2.13 (latest)●Since v1.0

# InterruptOnConfig

Configuration for an action requiring human in the loop.

This is the configuration format used in the `HumanInTheLoopMiddleware.__init__`
method.


```
InterruptOnConfig()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| allowed\_decisions | [list](https://docs.python.org/3/library/stdtypes.html#list)[[DecisionType](/python/langchain/agents/middleware/human_in_the_loop/DecisionType)] |
| description | NotRequired[[str](https://docs.python.org/3/library/stdtypes.html#str) | \_DescriptionFactory] |
| args\_schema | NotRequired[[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]] |

## Attributes

[attribute

allowed\_decisions: list[DecisionType]

The decisions that are allowed for this action.](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig/allowed_decisions)[attribute

description: NotRequired[str | \_DescriptionFactory]

The description attached to the request for human input.

Can be either:

- A static string describing the approval request
- A callable that dynamically generates the description based on agent state,
  runtime, and tool call information](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig/description)[attribute

args\_schema: NotRequired[dict[str, Any]]

JSON schema for the args associated with the action, if edits are allowed.](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig/args_schema)


