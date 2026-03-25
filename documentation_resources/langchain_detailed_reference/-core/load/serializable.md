<!-- Source: https://reference.langchain.com/python/langchain-core/load/serializable -->

Modulev1.2.21 (latest)●Since v0.1

# serializable

Serializable base class.

## Attributes

[attribute

logger](/python/langchain-core/load/serializable/logger)

## Functions

[function

try\_neq\_default

Try to determine if a value is different from the default.](/python/langchain-core/load/serializable/try_neq_default)[function

to\_json\_not\_implemented

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/to_json_not_implemented)

## Classes

[class

BaseSerialized

Base class for serialized objects.](/python/langchain-core/load/serializable/BaseSerialized)[class

SerializedConstructor

Serialized constructor.](/python/langchain-core/load/serializable/SerializedConstructor)[class

SerializedSecret

Serialized secret.](/python/langchain-core/load/serializable/SerializedSecret)[class

SerializedNotImplemented

Serialized not implemented.](/python/langchain-core/load/serializable/SerializedNotImplemented)[class

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
  as part of the serialized representation.](/python/langchain-core/load/serializable/Serializable)


