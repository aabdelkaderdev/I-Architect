<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/in_memory -->

Modulev1.2.21 (latest)●Since v0.2

# in\_memory

In-memory vector store.

## Functions

## Classes

## Modules



[function

dumpd](/python/langchain-core/load/dump/dumpd)

[function

cosine\_similarity](/python/langchain-core/vectorstores/in_memory/cosine_similarity)

[function

maximal\_marginal\_relevance](/python/langchain-core/vectorstores/utils/maximal_marginal_relevance)

[class

Document](/python/langchain-core/documents/base/Document)

[class

VectorStore](/python/langchain-core/vectorstores/base/VectorStore)

[class

Embeddings](/python/langchain-core/embeddings/embeddings/Embeddings)

[class

InMemoryVectorStore](/python/langchain-core/vectorstores/in_memory/InMemoryVectorStore)

[module

load](/python/langchain-core/load/load)

Return a dict representation of an object.

Calculate maximal marginal relevance.

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.

Interface for vector store.

Interface for embedding models.

This is an interface meant for implementing text embedding models.

Text embedding models are used to map text to a vector (a point in n-dimensional
space).

Texts that are similar will usually be mapped to points that are close to each
other in this space. The exact details of what's considered "similar" and how
"distance" is measured in this space are dependent on the specific embedding model.

This abstraction contains a method for embedding a list of documents and a method
for embedding a query text. The embedding of a query text is expected to be a single
vector, while the embedding of a list of documents is expected to be a list of
vectors.

Usually the query embedding is identical to the document embedding, but the
abstraction allows treating them independently.

In addition to the synchronous methods, this interface also provides asynchronous
versions of the methods.

By default, the asynchronous methods are implemented using the synchronous methods;
however, implementations may choose to override the asynchronous methods with
an async native implementation for performance reasons.

In-memory vector store implementation.

Uses a dictionary, and computes cosine similarity for search using numpy.

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