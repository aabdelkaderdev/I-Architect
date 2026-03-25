<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HITLRequest -->

Classv1.2.13 (latest)●Since v1.0

# HITLRequest

Request for human feedback on a sequence of actions requested by a model.


```
HITLRequest()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| action\_requests | [list](https://docs.python.org/3/library/stdtypes.html#list)[[ActionRequest](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest)] |
| review\_configs | [list](https://docs.python.org/3/library/stdtypes.html#list)[[ReviewConfig](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig)] |

## Attributes

[attribute

action\_requests: list[ActionRequest]

A list of agent actions for human review.](/python/langchain/agents/middleware/human_in_the_loop/HITLRequest/action_requests)[attribute

review\_configs: list[ReviewConfig]

Review configuration for all possible actions.](/python/langchain/agents/middleware/human_in_the_loop/HITLRequest/review_configs)


