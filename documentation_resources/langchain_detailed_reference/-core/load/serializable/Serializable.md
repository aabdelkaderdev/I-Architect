<!-- Source: https://reference.langchain.com/python/langchain-core/load/serializable/Serializable -->

Classv1.2.21 (latest)●Since v0.1

# Serializable

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
  as part of the serialized representation.


```
Serializable(
    self,
    *args: Any = (),
    **kwargs: Any = {},
)
```

## Bases

`BaseModel``ABC`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-core/load/serializable/Serializable/__init__)

## Attributes

[attribute

lc\_secrets: dict[str, str]

A map of constructor argument names to secret ids.

For example, `{"openai_api_key": "OPENAI_API_KEY"}`](/python/langchain-core/load/serializable/Serializable/lc_secrets)[attribute

lc\_attributes: dict

List of attribute names that should be included in the serialized kwargs.

These attributes must be accepted by the constructor.

Default is an empty dictionary.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[attribute

model\_config](/python/langchain-core/load/serializable/Serializable/model_config)

## Methods

[method

is\_lc\_serializable

Is this class serializable?

By design, even if a class inherits from `Serializable`, it is not serializable
by default. This is to prevent accidental serialization of objects that should
not be serialized.](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[method

get\_lc\_namespace

Get the namespace of the LangChain object.

The default implementation splits `cls.__module__` on `'.'`, e.g.
`langchain_openai.chat_models` becomes
`["langchain_openai", "chat_models"]`. This value is used by `lc_id` to
build the serialization identifier.

New partner packages should **not** override this method. The default
behavior is correct for any class whose module path already reflects
its package name. Some older packages (e.g. `langchain-openai`,
`langchain-anthropic`) override it to return a legacy-style namespace
like `["langchain", "chat_models", "openai"]`, matching the module
paths that existed before those integrations were split out of the
main `langchain` package. Those overrides are kept for
backwards-compatible deserialization; new packages should not copy them.

Deserialization mapping is handled separately by
`SERIALIZABLE_MAPPING` in `langchain_core.load.mapping`.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[method

lc\_id

Return a unique identifier for this class for serialization purposes.

The unique identifier is a list of strings that describes the path
to the object.

For example, for the class `langchain.llms.openai.OpenAI`, the id is
`["langchain", "llms", "openai", "OpenAI"]`.](/python/langchain-core/load/serializable/Serializable/lc_id)[method

to\_json

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[method

to\_json\_not\_implemented

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


