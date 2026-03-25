<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Base classes for indexing.

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

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

BaseRetriever

Abstract base class for a document retrieval system.

A retrieval system is defined as something that can take string queries and return
the most 'relevant' documents from some source.

Usage:

A retriever follows the standard `Runnable` interface, and should be used via the
standard `Runnable` methods of `invoke`, `ainvoke`, `batch`, `abatch`.

Implementation:

When implementing a custom retriever, the class should implement the
`_get_relevant_documents` method to define the logic for retrieving documents.

Optionally, an async native implementations can be provided by overriding the
`_aget_relevant_documents` method.

Retriever that returns the first 5 documents from a list of documents

```
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

class SimpleRetriever(BaseRetriever):
    docs: list[Document]
    k: int = 5

    def _get_relevant_documents(self, query: str) -> list[Document]:
        """Return the first k documents from the list of documents"""
        return self.docs[:self.k]

    async def _aget_relevant_documents(self, query: str) -> list[Document]:
        """(Optional) async native implementation."""
        return self.docs[:self.k]
```

Simple retriever based on a scikit-learn vectorizer

```
from sklearn.metrics.pairwise import cosine_similarity

class TFIDFRetriever(BaseRetriever, BaseModel):
    vectorizer: Any
    docs: list[Document]
    tfidf_array: Any
    k: int = 4

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> list[Document]:
        # Ip -- (n_docs,x), Op -- (n_docs,n_Feats)
        query_vec = self.vectorizer.transform([query])
        # Op -- (n_docs,1) -- Cosine Sim with each doc
        results = cosine_similarity(self.tfidf_array, query_vec).reshape((-1,))
        return [self.docs[i] for i in results.argsort()[-self.k :][::-1]]
```](/python/langchain-core/retrievers/BaseRetriever)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

RecordManager

Abstract base class representing the interface for a record manager.

The record manager abstraction is used by the langchain indexing API.

The record manager keeps track of which documents have been
written into a `VectorStore` and when they were written.

The indexing API computes hashes for each document and stores the hash
together with the write time and the source id in the record manager.

On subsequent indexing runs, the indexing API can check the record manager
to determine which documents have already been indexed and which have not.

This allows the indexing API to avoid re-indexing documents that have
already been indexed, and to only index new documents.

The main benefit of this abstraction is that it works across many vectorstores.
To be supported, a `VectorStore` needs to only support the ability to add and
delete documents by ID. Using the record manager, the indexing API will
be able to delete outdated documents and avoid redundant indexing of documents
that have already been indexed.

The main constraints of this abstraction are:

1. It relies on the time-stamps to determine which documents have been
   indexed and which have not. This means that the time-stamps must be
   monotonically increasing. The timestamp should be the timestamp
   as measured by the server to minimize issues.
2. The record manager is currently implemented separately from the
   vectorstore, which means that the overall system becomes distributed
   and may create issues with consistency. For example, writing to
   record manager succeeds, but corresponding writing to `VectorStore` fails.](/python/langchain-core/indexing/base/RecordManager)[class

InMemoryRecordManager

An in-memory record manager for testing purposes.](/python/langchain-core/indexing/base/InMemoryRecordManager)[class

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
3. Searching for document using a query.](/python/langchain-core/indexing/base/DocumentIndex)


