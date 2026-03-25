<!-- Source: https://reference.langchain.com/python/langchain-core/utils/json_schema/dereference_refs -->

Functionv1.2.21 (latest)●Since v0.1

# dereference\_refs

Resolve and inline JSON Schema `$ref` references in a schema object.

This function processes a JSON Schema and resolves all `$ref` references by
replacing them with the actual referenced content.

Handles both simple references and complex cases like circular references and mixed
`$ref` objects that contain additional properties alongside the `$ref`.


```
dereference_refs(
  schema_obj: dict,
  *,
  full_schema: dict | None = None,
  skip_keys: Sequence[str] | None = None
) -> dict
```

- Circular references are handled gracefully by breaking cycles
- Mixed `$ref` objects (with both `$ref` and other properties) are supported
- Additional properties in mixed `$refs` override resolved properties
- The `$defs` section is preserved in the output by default

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `schema_obj`\* | `dict` | The JSON Schema object or fragment to process.  This can be a complete schema or just a portion of one. |
| `full_schema` | `dict | None` | Default:`None`  The complete schema containing all definitions that `$refs` might point to.  If not provided, defaults to `schema_obj` (useful when the schema is self-contained). |
| `skip_keys` | `Sequence[str] | None` | Default:`None`  Controls recursion behavior and reference resolution depth.   - If `None` (Default): Only recurse under `'$defs'` and use shallow   reference resolution (break cycles but don't deep-inline nested refs) - If provided (even as `[]`): Recurse under all keys and use deep reference   resolution (fully inline all nested references) |


