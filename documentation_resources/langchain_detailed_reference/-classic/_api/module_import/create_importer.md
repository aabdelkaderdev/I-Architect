<!-- Source: https://reference.langchain.com/python/langchain-classic/_api/module_import/create_importer -->

Functionv1.2.13 (latest)●Since v1.0

# create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).


```
create_importer(
  package: str,
  *,
  module_lookup: dict[str, str] | None = None,
  deprecated_lookups: dict[str, str] | None = None,
  fallback_module: str | None = None
) -> Callable[[str], Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `package`\* | `str` | Current package. Use `__package__` |
| `module_lookup` | `dict[str, str] | None` | Default:`None`  Maps name of object to the module where it is defined. e.g.,   ``` {     "MyDocumentLoader": (         "langchain_community.document_loaders.my_document_loader"     ) } ``` |
| `deprecated_lookups` | `dict[str, str] | None` | Default:`None`  Same as module look up, but will raise deprecation warnings. |
| `fallback_module` | `str | None` | Default:`None`  Module to import from if the object is not found in `module_lookup` or if `module_lookup` is not provided. |


