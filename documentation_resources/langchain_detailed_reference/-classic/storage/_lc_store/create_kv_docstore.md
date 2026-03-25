<!-- Source: https://reference.langchain.com/python/langchain-classic/storage/_lc_store/create_kv_docstore -->

Functionv1.2.13 (latest)●Since v1.0

# create\_kv\_docstore

Create a store for langchain `Document` objects from a bytes store.

This store does run time type checking to ensure that the values are
`Document` objects.


```
create_kv_docstore(
  store: ByteStore,
  *,
  key_encoder: Callable[[str], str] | None = None
) -> BaseStore[str, Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `store`\* | `ByteStore` | A bytes store to use as the underlying store. |
| `key_encoder` | `Callable[[str], str] | None` | Default:`None`  A function to encode keys; if `None`, uses identity function. |


