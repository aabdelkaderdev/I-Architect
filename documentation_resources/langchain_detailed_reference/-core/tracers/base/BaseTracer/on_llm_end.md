<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_llm_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_end

End a trace for an LLM or chat model run.


```
on_llm_end(
  self,
  response: LLMResult,
  *,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

**Note:**

This is the end callback for both run types. Chat models start with
`on_chat_model_start`, but there is no `on_chat_model_end`;
completion is routed here for callback API compatibility.

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `response`\* | `LLMResult` | The response. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


