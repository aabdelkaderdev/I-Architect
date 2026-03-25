<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/_lc_store/create_lc_store -->

Functionv1.2.13 (latest)●Since v1.0

# create\_lc\_store

Create a store for LangChain serializable objects from a bytes store.


```
create_lc_store(
  store: ByteStore,
  *,
  key_encoder: Callable[[str], str] | None = None
) -> BaseStore[str, Serializable]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `store`\* | `ByteStore` | A bytes store to use as the underlying store. |
| `key_encoder` | `Callable[[str], str] | None` | Default:`None`  A function to encode keys; if `None` uses identity function. |


