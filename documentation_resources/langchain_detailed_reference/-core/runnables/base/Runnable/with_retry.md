<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_retry -->

Methodv1.2.21 (latest)●Since v0.1

# with\_retry

Create a new `Runnable` that retries the original `Runnable` on exceptions.


```
with_retry(
  self,
  *,
  retry_if_exception_type: tuple[type[BaseException], ...] = (Exception,),
  wait_exponential_jitter: bool = True,
  exponential_jitter_params: ExponentialJitterParams | None = None,
  stop_after_attempt: int = 3
) -> Runnable[Input, Output]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda

count = 0

def _lambda(x: int) -> None:
    global count
    count = count + 1
    if x == 1:
        raise ValueError("x is 1")
    else:
        pass

runnable = RunnableLambda(_lambda)
try:
    runnable.with_retry(
        stop_after_attempt=2,
        retry_if_exception_type=(ValueError,),
    ).invoke(1)
except ValueError:
    pass

assert count == 2
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `retry_if_exception_type` | `tuple[type[BaseException], ...]` | Default:`(Exception,)`  A tuple of exception types to retry on. |
| `wait_exponential_jitter` | `bool` | Default:`True`  Whether to add jitter to the wait time between retries. |
| `stop_after_attempt` | `int` | Default:`3`  The maximum number of attempts to make before giving up. |
| `exponential_jitter_params` | `ExponentialJitterParams | None` | Default:`None`  Parameters for `tenacity.wait_exponential_jitter`. Namely: `initial`, `max`, `exp_base`, and `jitter` (all `float` values). |


