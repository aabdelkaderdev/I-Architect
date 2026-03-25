<!-- Source: https://reference.langchain.com/python/langchain-core/load/load/Reviver -->

Classv1.2.21 (latest)●Since v0.1

# Reviver

Reviver for JSON objects.

Used as the `object_hook` for `json.loads` to reconstruct LangChain objects from
their serialized JSON representation.

Only classes in the allowlist can be instantiated.


```
Reviver(
  self,
  allowed_objects: Iterable[AllowedObject] | Literal['all', 'core'] = 'core',
  secrets_map: dict[str, str] | None = None,
  valid_namespaces: list[str] | None = None,
  secrets_from_env: bool = False,
  additional_import_mappings: dict[tuple[str, ...], tuple[str, ...]] | None = None,
  *,
  ignore_unserializable_fields: bool = False,
  init_validator: InitValidator | None = default_init_validator
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `allowed_objects` | `Iterable[AllowedObject] | Literal['all', 'core']` | Default:`'core'`  Allowlist of classes that can be deserialized.   - `'core'` (default): Allow classes defined in the serialization   mappings for `langchain_core`. - `'all'`: Allow classes defined in the serialization mappings.  This includes core LangChain types (messages, prompts, documents,   etc.) and trusted partner integrations. See   `langchain_core.load.mapping` for the full list. - Explicit list of classes: Only those specific classes are allowed. |
| `secrets_map` | `dict[str, str] | None` | Default:`None`  A map of secrets to load.  Only include the specific secrets the serialized object requires. If a secret is not found in the map, it will be loaded from the environment if `secrets_from_env` is `True`. |
| `valid_namespaces` | `list[str] | None` | Default:`None`  Additional namespaces (modules) to allow during deserialization, beyond the default trusted namespaces. |
| `secrets_from_env` | `bool` | Default:`False`  Whether to load secrets from the environment.  A crafted payload can name arbitrary environment variables in its `secret` fields, so enabling this on untrusted data can leak sensitive values. Keep this `False` (the default) unless the serialized data is fully trusted. |
| `additional_import_mappings` | `dict[tuple[str, ...], tuple[str, ...]] | None` | Default:`None`  A dictionary of additional namespace mappings.  You can use this to override default mappings or add new mappings.  When `allowed_objects` is `None` (using defaults), paths from these mappings are also added to the allowed class paths. |
| `ignore_unserializable_fields` | `bool` | Default:`False`  Whether to ignore unserializable fields. |
| `init_validator` | `InitValidator | None` | Default:`default_init_validator`  Optional callable to validate kwargs before instantiation.  If provided, this function is called with `(class_path, kwargs)` where `class_path` is the class path tuple and `kwargs` is the kwargs dict. The validator should raise an exception if the object should not be deserialized, otherwise return `None`.  Defaults to `default_init_validator` which blocks jinja2 templates. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| allowed\_objects | [Iterable](https://docs.python.org/3/library/typing.html#typing.Iterable)[[AllowedObject](/python/langchain-core/load/load/AllowedObject)] | [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['all', 'core'] |
| secrets\_map | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| valid\_namespaces | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| secrets\_from\_env | [bool](https://docs.python.org/3/library/functions.html#bool) |
| additional\_import\_mappings | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...], [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]] | None |
| ignore\_unserializable\_fields | [bool](https://docs.python.org/3/library/functions.html#bool) |
| init\_validator | [InitValidator](/python/langchain-core/load/load/InitValidator) | None |

## Attributes

[attribute

secrets\_from\_env: secrets\_from\_env](/python/langchain-core/load/load/Reviver/secrets_from_env)[attribute

secrets\_map](/python/langchain-core/load/load/Reviver/secrets_map)[attribute

valid\_namespaces: list](/python/langchain-core/load/load/Reviver/valid_namespaces)[attribute

additional\_import\_mappings](/python/langchain-core/load/load/Reviver/additional_import_mappings)[attribute

import\_mappings: dict](/python/langchain-core/load/load/Reviver/import_mappings)[attribute

allowed\_class\_paths: set[tuple[str, ...]] | None](/python/langchain-core/load/load/Reviver/allowed_class_paths)[attribute

ignore\_unserializable\_fields: ignore\_unserializable\_fields](/python/langchain-core/load/load/Reviver/ignore_unserializable_fields)[attribute

init\_validator: init\_validator](/python/langchain-core/load/load/Reviver/init_validator)


