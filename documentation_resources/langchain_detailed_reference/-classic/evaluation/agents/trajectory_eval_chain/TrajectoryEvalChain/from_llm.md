<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a TrajectoryEvalChain object from a language model chain.


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  agent_tools: Sequence[BaseTool] | None = None,
  output_parser: TrajectoryOutputParser | None = None,
  **kwargs: Any = {}
) -> TrajectoryEvalChain
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model chain. |
| `agent_tools` | `Sequence[BaseTool] | None` | Default:`None`  A list of tools available to the agent. |
| `output_parser` \* | `unknown` | The output parser used to parse the chain output into a score. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


