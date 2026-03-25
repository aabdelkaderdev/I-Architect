<!-- Source: https://reference.langchain.com/python/langchain-core/utils/strings/sanitize_for_postgres -->

Functionv1.2.21 (latest)●Since v0.3

# sanitize\_for\_postgres

Sanitize text by removing NUL bytes that are incompatible with PostgreSQL.

PostgreSQL text fields cannot contain `NUL (0x00)` bytes, which can cause
`psycopg.DataError` when inserting documents. This function removes or replaces
such characters to ensure compatibility.


```
sanitize_for_postgres(
    text: str,
    replacement: str = '',
) -> str
```

**Example:**

> > > sanitize\_for\_postgres("Hello\x00world")
> > > 'Helloworld'
> > > sanitize\_for\_postgres("Hello\x00world", " ")
> > > 'Hello world'

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text to sanitize. |
| `replacement` | `str` | Default:`''`  String to replace `NUL` bytes with. |


