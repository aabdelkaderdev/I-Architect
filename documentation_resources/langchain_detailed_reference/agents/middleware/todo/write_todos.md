<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/todo/write_todos -->

Functionv1.2.13 (latest)●Since v1.0

# write\_todos

Create and manage a structured task list for your current work session.


```
write_todos(
  todos: list[Todo],
  tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command[Any]
```


