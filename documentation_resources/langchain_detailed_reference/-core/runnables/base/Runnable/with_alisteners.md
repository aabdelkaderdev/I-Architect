<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_alisteners -->

Methodv1.2.21 (latest)●Since v0.2

# with\_alisteners

Bind async lifecycle listeners to a `Runnable`.

Returns a new `Runnable`.

The Run object contains information about the run, including its `id`,
`type`, `input`, `output`, `error`, `start_time`, `end_time`, and
any tags or metadata added to the run.


```
with_alisteners(
  self,
  *,
  on_start: AsyncListener | None = None,
  on_end: AsyncListener | None = None,
  on_error: AsyncListener | None = None
) -> Runnable[Input, Output]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda, Runnable
from datetime import datetime, timezone
import time
import asyncio

def format_t(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

async def test_runnable(time_to_sleep: int):
    print(f"Runnable[{time_to_sleep}s]: starts at {format_t(time.time())}")
    await asyncio.sleep(time_to_sleep)
    print(f"Runnable[{time_to_sleep}s]: ends at {format_t(time.time())}")

async def fn_start(run_obj: Runnable):
    print(f"on start callback starts at {format_t(time.time())}")
    await asyncio.sleep(3)
    print(f"on start callback ends at {format_t(time.time())}")

async def fn_end(run_obj: Runnable):
    print(f"on end callback starts at {format_t(time.time())}")
    await asyncio.sleep(2)
    print(f"on end callback ends at {format_t(time.time())}")

runnable = RunnableLambda(test_runnable).with_alisteners(
    on_start=fn_start, on_end=fn_end
)

async def concurrent_runs():
    await asyncio.gather(runnable.ainvoke(2), runnable.ainvoke(3))

asyncio.run(concurrent_runs())
# Result:
# on start callback starts at 2025-03-01T07:05:22.875378+00:00
# on start callback starts at 2025-03-01T07:05:22.875495+00:00
# on start callback ends at 2025-03-01T07:05:25.878862+00:00
# on start callback ends at 2025-03-01T07:05:25.878947+00:00
# Runnable[2s]: starts at 2025-03-01T07:05:25.879392+00:00
# Runnable[3s]: starts at 2025-03-01T07:05:25.879804+00:00
# Runnable[2s]: ends at 2025-03-01T07:05:27.881998+00:00
# on end callback starts at 2025-03-01T07:05:27.882360+00:00
# Runnable[3s]: ends at 2025-03-01T07:05:28.881737+00:00
# on end callback starts at 2025-03-01T07:05:28.882428+00:00
# on end callback ends at 2025-03-01T07:05:29.883893+00:00
# on end callback ends at 2025-03-01T07:05:30.884831+00:00
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `on_start` | `AsyncListener | None` | Default:`None`  Called asynchronously before the `Runnable` starts running, with the `Run` object. |
| `on_end` | `AsyncListener | None` | Default:`None`  Called asynchronously after the `Runnable` finishes running, with the `Run` object. |
| `on_error` | `AsyncListener | None` | Default:`None`  Called asynchronously if the `Runnable` throws an error, with the `Run` object. |


