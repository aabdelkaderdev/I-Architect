<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/map -->

Methodv1.2.21 (latest)●Since v0.1

# map

Return a new `Runnable` that maps a list of inputs to a list of outputs.

Calls `invoke` with each input.


```
map(
    self,
) -> Runnable[list[Input], list[Output]]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda

def _lambda(x: int) -> int:
    return x + 1

runnable = RunnableLambda(_lambda)
print(runnable.map().invoke([1, 2, 3]))  # [2, 3, 4]
```


