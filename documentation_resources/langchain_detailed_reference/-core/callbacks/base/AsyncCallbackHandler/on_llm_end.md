<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on_llm_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_llm\_end

Run when the model ends running.


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

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `response`\* | `LLMResult` | The response which was generated. |
| `run_id`\* | `UUID` | The ID of the current run. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


