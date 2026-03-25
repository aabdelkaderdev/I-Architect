<!-- Source: https://reference.langchain.com/python/langchain-core/load/load/loads -->

Functionv1.2.21 (latest)●Since v0.1

# loads

Revive a LangChain class from a JSON string.

Equivalent to `load(json.loads(text))`.

Only classes in the allowlist can be instantiated. The default allowlist includes
core LangChain types (messages, prompts, documents, etc.). See
`langchain_core.load.mapping` for the full list.

Do not use with untrusted input

This function instantiates Python objects and can trigger side effects
during deserialization. **Never call `loads()` on data from an untrusted
or unauthenticated source.** See the module-level security model
documentation for details and best practices.


```
loads(
  text: str,
  *,
  allowed_objects: Iterable[AllowedObject] | Literal['all', 'core'] = 'core',
  secrets_map: dict[str, str] | None = None,
  valid_namespaces: list[str] | None = None,
  secrets_from_env: bool = False,
  additional_import_mappings: dict[tuple[str, ...], tuple[str, ...]] | None = None,
  ignore_unserializable_fields: bool = False,
  init_validator: InitValidator | None = default_init_validator
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The string to load. |
| `allowed_objects` | `Iterable[AllowedObject] | Literal['all', 'core']` | Default:`'core'`  Allowlist of classes that can be deserialized.   - `'core'` (default): Allow classes defined in the serialization mappings   for `langchain_core`. - `'all'`: Allow classes defined in the serialization mappings.  This includes core LangChain types (messages, prompts, documents, etc.)   and trusted partner integrations. See `langchain_core.load.mapping` for   the full list. - Explicit list of classes: Only those specific classes are allowed. - `[]`: Disallow all deserialization (will raise on any object). |
| `secrets_map` | `dict[str, str] | None` | Default:`None`  A map of secrets to load.  Only include the specific secrets the serialized object requires. If a secret is not found in the map, it will be loaded from the environment if `secrets_from_env` is `True`. |
| `valid_namespaces` | `list[str] | None` | Default:`None`  Additional namespaces (modules) to allow during deserialization, beyond the default trusted namespaces. |
| `secrets_from_env` | `bool` | Default:`False`  Whether to load secrets from the environment.  A crafted payload can name arbitrary environment variables in its `secret` fields, so enabling this on untrusted data can leak sensitive values. Keep this `False` (the default) unless the serialized data is fully trusted. |
| `additional_import_mappings` | `dict[tuple[str, ...], tuple[str, ...]] | None` | Default:`None`  A dictionary of additional namespace mappings.  You can use this to override default mappings or add new mappings.  When `allowed_objects` is `None` (using defaults), paths from these mappings are also added to the allowed class paths. |
| `ignore_unserializable_fields` | `bool` | Default:`False`  Whether to ignore unserializable fields. |
| `init_validator` | `InitValidator | None` | Default:`default_init_validator`  Optional callable to validate kwargs before instantiation.  If provided, this function is called with `(class_path, kwargs)` where `class_path` is the class path tuple and `kwargs` is the kwargs dict. The validator should raise an exception if the object should not be deserialized, otherwise return `None`.  Defaults to `default_init_validator` which blocks jinja2 templates. |


