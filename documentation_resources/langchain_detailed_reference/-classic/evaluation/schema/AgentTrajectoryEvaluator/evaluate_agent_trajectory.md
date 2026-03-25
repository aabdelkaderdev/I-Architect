<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator/evaluate_agent_trajectory -->

Methodv1.2.13 (latest)●Since v1.0

# evaluate\_agent\_trajectory

Evaluate a trajectory.


```
evaluate_agent_trajectory(
  self,
  *,
  prediction: str,
  agent_trajectory: Sequence[tuple[AgentAction, str]],
  input: str,
  reference: str | None = None,
  **kwargs: Any = {}
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `prediction`\* | `str` | The final predicted response. |
| `agent_trajectory`\* | `Sequence[tuple[AgentAction, str]]` | The intermediate steps forming the agent trajectory. |
| `input`\* | `str` | The input to the agent. |
| `reference` | `str | None` | Default:`None`  The reference answer. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


