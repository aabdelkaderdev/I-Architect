<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/agent/Agent/get_full_inputs -->

Methodv1.2.13 (latest)●Since v1.0

# get\_full\_inputs


```
get_full_inputs(
  self,
  intermediate_steps: list[tuple[AgentAction, str]],
  **kwargs: Any
```



=

{

}

)

->

builtins

.

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[

[str](https://docs.python.org/3/library/stdtypes.html#str)

,

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

]

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` |  |
| `**kwargs` | `Any` | Default:`{}` |

Create the full inputs for the LLMChain from intermediate steps.

Steps the LLM has taken to date,
along with observations.

User inputs.