<!-- Source: https://reference.langchain.com/python/langchain-core/load/mapping -->

Modulev1.2.21 (latest)●Since v0.1

# mapping

Serialization mapping.

This file contains a mapping between the `lc_namespace` path for a given
subclass that implements from `Serializable` to the namespace
where that class is actually located.

This mapping helps maintain the ability to serialize and deserialize
well-known LangChain objects even if they are moved around in the codebase
across different LangChain versions.

For example, the code for the `AIMessage` class is located in
`langchain_core.messages.ai.AIMessage`. This message is associated with the
`lc_namespace` of `["langchain", "schema", "messages", "AIMessage"]`,
because this code was originally in `langchain.schema.messages.AIMessage`.

The mapping allows us to deserialize an `AIMessage` created with an older
version of LangChain where the code was in a different location.

## Attributes

[attribute

SERIALIZABLE\_MAPPING: dict[tuple[str, ...], tuple[str, ...]]](/python/langchain-core/load/mapping/SERIALIZABLE_MAPPING)[attribute

OLD\_CORE\_NAMESPACES\_MAPPING: dict[tuple[str, ...], tuple[str, ...]]](/python/langchain-core/load/mapping/OLD_CORE_NAMESPACES_MAPPING)


