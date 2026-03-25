<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/in_memory -->

Modulev1.2.21 (latest)●Since v0.2

# in\_memory

In memory document index.

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
`__init__` inheritance when installing its own (annotation-emitting) `C.__init__`).](/python/langchain-core/_api/beta_decorator/beta)

## Classes

[class

CallbackManagerForRetrieverRun

Callback manager for retriever run.](/python/langchain-core/callbacks/manager/CallbackManagerForRetrieverRun)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

UpsertResponse

A generic response for upsert operations.

The upsert response will be used by abstractions that implement an upsert
operation for content that can be upserted by ID.

Upsert APIs that accept inputs with IDs and generate IDs internally
will return a response that includes the IDs that succeeded and the IDs
that failed.

If there are no failures, the failed list will be empty, and the order
of the IDs in the succeeded list will match the order of the input documents.

If there are failures, the response becomes ill defined, and a user of the API
cannot determine which generated ID corresponds to which input document.

It is recommended for users explicitly attach the IDs to the items being
indexed to avoid this issue.](/python/langchain-core/indexing/base/UpsertResponse)[class

DeleteResponse

A generic response for delete operation.

The fields in this response are optional and whether the `VectorStore`
returns them or not is up to the implementation.](/python/langchain-core/indexing/base/DeleteResponse)[class

DocumentIndex

A document retriever that supports indexing operations.

This indexing interface is designed to be a generic abstraction for storing and
querying documents that has an ID and metadata associated with it.

The interface is designed to be agnostic to the underlying implementation of the
indexing system.

The interface is designed to support the following operations:

1. Storing document in the index.
2. Fetching document by ID.
3. Searching for document using a query.](/python/langchain-core/indexing/base/DocumentIndex)[class

InMemoryDocumentIndex

In memory document index.

This is an in-memory document index that stores documents in a dictionary.

It provides a simple search API that returns documents by the number of
counts the given query appears in the document.](/python/langchain-core/indexing/in_memory/InMemoryDocumentIndex)


