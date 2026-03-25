<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBindingBase/abatch_as_completed -->

Methodv1.2.21 (latest)●Since v0.1

# abatch\_as\_completed


```
abatch_as_completed(
  self,
  inputs: Sequence[Input],
  config: RunnableConfig | Sequence[RunnableConfig] | None = None,
  *,
  return_exceptions: bool = False,
  **kwargs: Any | None = {}
) -> AsyncIterator[tuple[int, Output | Exception]]
```


