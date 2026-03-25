<!-- Source: https://reference.langchain.com/python/langchain-core/load/load -->

Modulev1.2.21 (latest)●Since v0.1

# load

Load LangChain objects from JSON strings or objects.

## How it works

Each `Serializable` LangChain object has a unique identifier (its "class path"), which
is a list of strings representing the module path and class name. For example:

- `AIMessage` -> `["langchain_core", "messages", "ai", "AIMessage"]`
- `ChatPromptTemplate` -> `["langchain_core", "prompts", "chat", "ChatPromptTemplate"]`

When deserializing, the class path from the JSON `'id'` field is checked against an
allowlist. If the class is not in the allowlist, deserialization raises a `ValueError`.

## Security model

Exercise caution with untrusted input

These functions deserialize by instantiating Python objects, which means
constructors (`__init__`) and validators may run and can trigger side effects.
With the default settings, deserialization is restricted to a core allowlist
of `langchain_core` types (for example: messages, documents, and prompts)
defined in `langchain_core.load.mapping`.

If you broaden `allowed_objects` (for example, by using `'all'` or adding
additional classes), treat the serialized payload as a manifest and only
deserialize data that comes from a trusted source. A crafted payload that
is allowed to instantiate unintended classes could cause network calls,
file operations, or environment variable access during `__init__`.

The `allowed_objects` parameter controls which classes can be deserialized:

- **`'core'` (default)**: Allow classes defined in the serialization mappings for
  langchain\_core.
- **`'all'`**: Allow classes defined in the serialization mappings. This
  includes core LangChain types (messages, prompts, documents, etc.) and trusted
  partner integrations. See `langchain_core.load.mapping` for the full list.
- **Explicit list of classes**: Only those specific classes are allowed.

For simple data types like messages and documents, the default allowlist is safe to use.
These classes do not perform side effects during initialization.

Side effects in allowed classes

Deserialization calls `__init__` on allowed classes. If those classes perform side
effects during initialization (network calls, file operations, etc.), those side
effects will occur. The allowlist prevents instantiation of classes outside the
allowlist, but does not sandbox the allowed classes themselves.

Import paths are also validated against trusted namespaces before any module is
imported.

### Best practices

- Use the most restrictive `allowed_objects` possible. Prefer an explicit list
  of classes over `'core'` or `'all'`.
- Keep `secrets_from_env` set to `False` (the default). If you must use it,
  ensure the serialized data comes from a fully trusted source, as a crafted
  payload can read arbitrary environment variables.
- When using `secrets_map`, include only the specific secrets that the
  serialized object requires.

### Injection protection (escape-based)

During serialization, plain dicts that contain an `'lc'` key are escaped by wrapping
them: `{"__lc_escaped__": {...}}`. During deserialization, escaped dicts are unwrapped
and returned as plain dicts, NOT instantiated as LC objects.

This is an allowlist approach: only dicts explicitly produced by
`Serializable.to_json()` (which are NOT escaped) are treated as LC objects;
everything else is user data.

Even if an attacker's payload includes `__lc_escaped__` wrappers, it will be unwrapped
to plain dicts and NOT instantiated as malicious objects.

## Examples

```
from langchain_core.load import load
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

# Use default allowlist (classes from mappings) - recommended
obj = load(data)

# Allow only specific classes (most restrictive)
obj = load(
    data,
    allowed_objects=[
        ChatPromptTemplate,
        AIMessage,
        HumanMessage,
    ],
)
```

## Attributes

[attribute

OLD\_CORE\_NAMESPACES\_MAPPING: dict[tuple[str, ...], tuple[str, ...]]](/python/langchain-core/load/mapping/OLD_CORE_NAMESPACES_MAPPING)[attribute

SERIALIZABLE\_MAPPING: dict[tuple[str, ...], tuple[str, ...]]](/python/langchain-core/load/mapping/SERIALIZABLE_MAPPING)[attribute

DEFAULT\_NAMESPACES: list](/python/langchain-core/load/load/DEFAULT_NAMESPACES)[attribute

DISALLOW\_LOAD\_FROM\_PATH: list](/python/langchain-core/load/load/DISALLOW_LOAD_FROM_PATH)[attribute

ALL\_SERIALIZABLE\_MAPPINGS: dict](/python/langchain-core/load/load/ALL_SERIALIZABLE_MAPPINGS)[attribute

AllowedObject: type[Serializable]

Type alias for classes that can be included in the `allowed_objects` parameter.

Must be a `Serializable` subclass (the class itself, not an instance).](/python/langchain-core/load/load/AllowedObject)[attribute

InitValidator: Callable[[tuple[str, ...], dict[str, Any]], None]

Type alias for a callable that validates kwargs during deserialization.

The callable receives:

- `class_path`: A tuple of strings identifying the class being instantiated
  (e.g., `('langchain', 'schema', 'messages', 'AIMessage')`).
- `kwargs`: The kwargs dict that will be passed to the constructor.

The validator should raise an exception if the object should not be deserialized.](/python/langchain-core/load/load/InitValidator)

## Functions

[function

beta

Decorator to mark a function, a class, or a property as beta.

When marking a classmethod, a staticmethod, or a property, the `@beta` decorator
should go *under* `@classmethod` and `@staticmethod` (i.e., `beta` should directly
decorate the underlying callable), but *over* `@property`.

When marking a class `C` intended to be used as a base class in a multiple
inheritance hierarchy, `C` *must* define an `__init__` method (if `C` instead
inherited its `__init__` from its own base class, then `@beta` would mess up
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).](/python/langchain-core/_api/beta_decorator/beta)[function

default\_init\_validator

Default init validator that blocks jinja2 templates.

This is the default validator used by `load()` and `loads()` when no custom
validator is provided.](/python/langchain-core/load/load/default_init_validator)[function

loads

Revive a LangChain class from a JSON string.

Equivalent to `load(json.loads(text))`.

Only classes in the allowlist can be instantiated. The default allowlist includes
core LangChain types (messages, prompts, documents, etc.). See
`langchain_core.load.mapping` for the full list.

Do not use with untrusted input

This function instantiates Python objects and can trigger side effects
during deserialization. **Never call `loads()` on data from an untrusted
or unauthenticated source.** See the module-level security model
documentation for details and best practices.](/python/langchain-core/load/load/loads)[function

load

Revive a LangChain class from a JSON object.

Use this if you already have a parsed JSON object, eg. from `json.load` or
`orjson.loads`.

Only classes in the allowlist can be instantiated. The default allowlist includes
core LangChain types (messages, prompts, documents, etc.). See
`langchain_core.load.mapping` for the full list.

Do not use with untrusted input

This function instantiates Python objects and can trigger side effects
during deserialization. **Never call `load()` on data from an untrusted
or unauthenticated source.** See the module-level security model
documentation for details and best practices.](/python/langchain-core/load/load/load)

## Classes

[class

Serializable

Serializable base class.

This class is used to serialize objects to JSON.

It relies on the following methods and properties:

- [`is_lc_serializable`](/python/langchain-core/load/serializable/Serializable/is_lc_serializable): Is this class serializable?

  By design, even if a class inherits from `Serializable`, it is not serializable
  by default. This is to prevent accidental serialization of objects that should
  not be serialized.
- [`get_lc_namespace`](/python/langchain-core/load/serializable/Serializable/get_lc_namespace): Get the namespace of the LangChain object.

  During deserialization, this namespace is used to identify
  the correct class to instantiate.

  Please see the `Reviver` class in `langchain_core.load.load` for more details.

  During deserialization an additional mapping is handle classes that have moved
  or been renamed across package versions.
- [`lc_secrets`](/python/langchain-core/load/serializable/Serializable/lc_secrets): A map of constructor argument names to secret ids.
- [`lc_attributes`](/python/langchain-core/load/serializable/Serializable/lc_attributes): List of additional attribute names that should be included
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)[class

Reviver

Reviver for JSON objects.

Used as the `object_hook` for `json.loads` to reconstruct LangChain objects from
their serialized JSON representation.

Only classes in the allowlist can be instantiated.](/python/langchain-core/load/load/Reviver)


