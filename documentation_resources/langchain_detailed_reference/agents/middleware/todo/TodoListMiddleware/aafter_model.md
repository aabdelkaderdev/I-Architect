<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/todo/TodoListMiddleware/aafter_model -->

Methodv1.2.13 (latest)●Since v1.2

# aafter\_model

Check for parallel write\_todos tool calls and return errors if detected.

Async version of `after_model`. The todo list is designed to be updated at
most once per model turn. Since the `write_todos` tool replaces the entire
todo list with each call, making multiple parallel calls would create ambiguity
about which update should take precedence. This method prevents such conflicts
by rejecting any response that contains multiple write\_todos tool calls.


```
aafter_model(
  self,
  state: PlanningState[ResponseT],
  runtime: Runtime[ContextT]
) -> dict[str, Any] | None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `state`\* | `PlanningState[ResponseT]` | The current agent state containing messages. |
| `runtime`\* | `Runtime[ContextT]` | The LangGraph runtime instance. |


