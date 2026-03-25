<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/pipe -->

Methodv1.2.21 (latest)●Since v0.1

# pipe

Pipe `Runnable` objects.

Compose this `Runnable` with `Runnable`-like objects to make a
`RunnableSequence`.

Equivalent to `RunnableSequence(self, *others)` or `self | others[0] | ...`


```
pipe(
  self,
  *others: Runnable[Any, Other] | Callable[[Any], Other] = (),
  name: str | None = None
) -> RunnableSerializable[Input, Other]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
sequence = runnable_1.pipe(runnable_2)
# Or equivalently:
# sequence = runnable_1 | runnable_2
# sequence = RunnableSequence(first=runnable_1, last=runnable_2)
sequence.invoke(1)
await sequence.ainvoke(1)
# -> 4

sequence.batch([1, 2, 3])
await sequence.abatch([1, 2, 3])
# -> [4, 6, 8]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `*others` | `Runnable[Any, Other] | Callable[[Any], Other]` | Default:`()`  Other `Runnable` or `Runnable`-like objects to compose |
| `name` | `str | None` | Default:`None`  An optional name for the resulting `RunnableSequence`. |


