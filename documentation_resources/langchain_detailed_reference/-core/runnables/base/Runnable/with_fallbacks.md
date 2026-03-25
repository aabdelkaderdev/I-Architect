<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/with_fallbacks -->

Methodv1.2.21 (latest)●Since v0.1

# with\_fallbacks

Add fallbacks to a `Runnable`, returning a new `Runnable`.

The new `Runnable` will try the original `Runnable`, and then each fallback
in order, upon failures.


```
with_fallbacks(
  self,
  fallbacks: Sequence[Runnable[Input, Output]],
  *,
  exceptions_to_handle: tuple[type[BaseException], ...] = (Exception,),
  exception_key: str | None = None
) -> RunnableWithFallbacksT[Input, Output]
```

**Example:**

```
from typing import Iterator

from langchain_core.runnables import RunnableGenerator

def _generate_immediate_error(input: Iterator) -> Iterator[str]:
    raise ValueError()
    yield ""

def _generate(input: Iterator) -> Iterator[str]:
    yield from "foo bar"

runnable = RunnableGenerator(_generate_immediate_error).with_fallbacks(
    [RunnableGenerator(_generate)]
)
print("".join(runnable.stream({})))  # foo bar
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `fallbacks`\* | `Sequence[Runnable[Input, Output]]` | A sequence of runnables to try if the original `Runnable` fails. |
| `exceptions_to_handle` | `tuple[type[BaseException], ...]` | Default:`(Exception,)`  A tuple of exception types to handle. |
| `exception_key` | `str | None` | Default:`None`  If `string` is specified then handled exceptions will be passed to fallbacks as part of the input under the specified key.  If `None`, exceptions will not be passed to fallbacks.  If used, the base `Runnable` and its fallbacks must accept a dictionary as input. |
| `fallbacks`\* | `Sequence[Runnable[Input, Output]]` | A sequence of runnables to try if the original `Runnable` fails. |
| `exceptions_to_handle` | `tuple[type[BaseException], ...]` | Default:`(Exception,)`  A tuple of exception types to handle. |
| `exception_key` | `str | None` | Default:`None`  If `string` is specified then handled exceptions will be passed to fallbacks as part of the input under the specified key.  If `None`, exceptions will not be passed to fallbacks.  If used, the base `Runnable` and its fallbacks must accept a dictionary as input. |


