<!-- Source: https://reference.langchain.com/python/langchain-core/utils/json_schema -->

Modulev1.2.21 (latest)●Since v0.1

# json\_schema

Utilities for JSON Schema.

## Functions

[function

dereference\_refs

Resolve and inline JSON Schema `$ref` references in a schema object.

This function processes a JSON Schema and resolves all `$ref` references by
replacing them with the actual referenced content.

Handles both simple references and complex cases like circular references and mixed
`$ref` objects that contain additional properties alongside the `$ref`.](/python/langchain-core/utils/json_schema/dereference_refs)


