<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_llm_start -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_start

Run when LLM starts running.


```
on_llm_start(
  self,
  serialized: dict[str, Any],
  prompts: list[str],
  run_id: UUID | None = None,
  **kwargs: Any = {}
) -> list[AsyncCallbackManagerForLLMRun]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `serialized`\* | `dict[str, Any]` | The serialized LLM. |
| `prompts`\* | `list[str]` | The list of prompts. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


