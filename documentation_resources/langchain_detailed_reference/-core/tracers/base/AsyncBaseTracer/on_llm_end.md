<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/AsyncBaseTracer/on_llm_end -->

Methodv1.2.21 (latest)●Since v0.2

# on\_llm\_end

End a trace for an LLM or chat model run.


```
on_llm_end(
  self,
  response: LLMResult,
  *,
  run_id: UUID,
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  **kwargs: Any = {}
) -> None
```

**Note:**

This async callback also handles both run types. Async chat models
start with `on_chat_model_start`, but there is no
`on_chat_model_end`; completion is routed here for callback API
compatibility.


