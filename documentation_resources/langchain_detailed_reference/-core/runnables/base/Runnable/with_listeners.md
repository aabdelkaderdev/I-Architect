<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_listeners -->

Methodv1.2.21 (latest)●Since v0.1

# with\_listeners

Bind lifecycle listeners to a `Runnable`, returning a new `Runnable`.

The Run object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.


```
with_listeners(
  self,
  *,
  on_start: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None,
  on_end: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None,
  on_error: Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None = None
) -> Runnable[Input, Output]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda
from langchain_core.tracers.schemas import Run

import time

def test_runnable(time_to_sleep: int):
    time.sleep(time_to_sleep)

def fn_start(run_obj: Run):
    print("start_time:", run_obj.start_time)

def fn_end(run_obj: Run):
    print("end_time:", run_obj.end_time)

chain = RunnableLambda(test_runnable).with_listeners(
    on_start=fn_start, on_end=fn_end
)
chain.invoke(2)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `on_start` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called before the `Runnable` starts running, with the `Run` object. |
| `on_end` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called after the `Runnable` finishes running, with the `Run` object. |
| `on_error` | `Callable[[Run], None] | Callable[[Run, RunnableConfig], None] | None` | Default:`None`  Called if the `Runnable` throws an error, with the `Run` object. |


