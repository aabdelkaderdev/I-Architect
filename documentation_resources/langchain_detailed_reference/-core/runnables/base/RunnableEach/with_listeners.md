<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableEach/with_listeners -->

Methodv1.2.21 (latest)●Since v0.1

# with\_listeners

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.

The `Run` object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.


```
with_listeners(
  self,
  *,
  on_start: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None,
  on_end: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None,
  on_error: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None
) -> RunnableEach[Input, Output]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `on_start` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called before the `Runnable` starts running, with the `Run` object. |
| `on_end` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called after the `Runnable` finishes running, with the `Run` object. |
| `on_error` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called if the `Runnable` throws an error, with the `Run` object. |


