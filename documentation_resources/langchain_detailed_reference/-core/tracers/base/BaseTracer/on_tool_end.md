<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/base/BaseTracer/on_tool_end -->

Methodv1.2.21 (latest)●Since v0.1

# on\_tool\_end

End a trace for a tool run.


```
on_tool_end(
  self,
  output: Any,
  *,
  run_id: UUID,
  **kwargs: Any = {}
) -> Run
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `output`\* | `Any` | The output for the tool. |
| `run_id`\* | `UUID` | The run ID. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


