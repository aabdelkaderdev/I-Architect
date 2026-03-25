<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/combine_documents/reduce/split_list_of_docs -->

Functionv1.2.13 (latest)●Since v1.0

# split\_list\_of\_docs

Split `Document` objects to subsets that each meet a cumulative len. constraint.


```
split_list_of_docs(
  docs: list[Document],
  length_func: Callable,
  token_max: int,
  **kwargs: Any = {}
) -> list[list[Document]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs`\* | `list[Document]` | The full list of `Document` objects. |
| `length_func`\* | `Callable` | Function for computing the cumulative length of a set of `Document` objects. |
| `token_max`\* | `int` | The maximum cumulative length of any subset of `Document` objects. |
| `**kwargs` | `Any` | Default:`{}`  Arbitrary additional keyword params to pass to each call of the `length_func`. |


