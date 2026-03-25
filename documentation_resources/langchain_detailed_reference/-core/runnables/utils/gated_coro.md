<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils/gated_coro -->

Functionv1.2.21 (latest)●Since v0.1

# gated\_coro

Run a coroutine with a semaphore.


```
gated_coro(
    semaphore: asyncio.Semaphore,
    coro: Coroutine,
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `semaphore`\* | `asyncio.Semaphore` | The semaphore to use. |
| `coro`\* | `Coroutine` | The coroutine to run. |


