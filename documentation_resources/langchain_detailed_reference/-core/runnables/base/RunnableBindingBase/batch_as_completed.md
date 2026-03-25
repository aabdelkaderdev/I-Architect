<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBindingBase/batch_as_completed -->

Methodv1.2.21 (latest)●Since v0.1

# batch\_as\_completed


```
batch_as_completed(
  self,
  inputs: Sequence[Input],
  config: RunnableConfig | Sequence[RunnableConfig] | None = None,
  *,
  return_exceptions: bool = False,
  **kwargs: Any | None = {}
) -> Iterator[tuple[int, Output | Exception]]
```


