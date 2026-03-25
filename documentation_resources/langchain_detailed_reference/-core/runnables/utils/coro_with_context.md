<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils/coro_with_context -->

Functionv1.2.21 (latest)●Since v0.3

# coro\_with\_context

Await a coroutine with a context.


```
coro_with_context(
  coro: Awaitable[_T],
  context: Context,
  *,
  create_task: bool = False
) -> Awaitable[_T]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `coro`\* | `Awaitable[_T]` | The coroutine to await. |
| `context`\* | `Context` | The context to use. |
| `create_task` | `bool` | Default:`False`  Whether to create a task. |


