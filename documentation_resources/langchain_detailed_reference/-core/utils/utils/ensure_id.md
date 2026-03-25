<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/ensure_id -->

Functionv1.2.21 (latest)●Since v1.0

# ensure\_id

Ensure the ID is a valid string, generating a new UUID if not provided.

Auto-generated UUIDs are prefixed by `'lc_'` to indicate they are
LangChain-generated IDs.


```
ensure_id(
    id_val: str | None,
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `id_val`\* | `str | None` | Optional string ID value to validate. |


