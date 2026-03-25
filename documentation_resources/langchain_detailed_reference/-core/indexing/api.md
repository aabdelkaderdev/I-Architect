<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/api -->

Modulev1.2.21 (latest)●Since v0.1

# api

Module contains logic for indexing documents into vector stores.

## Attributes

[attribute

NAMESPACE\_UUID](/python/langchain-core/indexing/api/NAMESPACE_UUID)[attribute

T](/python/langchain-core/indexing/api/T)

## Functions

[function

index

Index data from the loader into the vector store.

Indexing functionality uses a manager to keep track of which documents
are in the vector store.

This allows us to keep track of which documents were updated, and which
documents were deleted, which documents should be skipped.

For the time being, documents are indexed using their hashes, and users
are not able to specify the uid of the document.

Behavior changed in `langchain-core` 0.3.25

Added `scoped_full` cleanup mode.

Warning

- In full mode, the loader should be returning
  the entire dataset, and not just a subset of the dataset.
  Otherwise, the auto\_cleanup will remove documents that it is not
  supposed to.
- In incremental mode, if documents associated with a particular
  source id appear across different batches, the indexing API
  will do some redundant work. This will still result in the
  correct end state of the index, but will unfortunately not be
  100% efficient. For example, if a given document is split into 15
  chunks, and we index them using a batch size of 5, we'll have 3 batches
  all with the same source id. In general, to avoid doing too much
  redundant work select as big a batch size as possible.
- The `scoped_full` mode is suitable if determining an appropriate batch size
  is challenging or if your data loader cannot return the entire dataset at
  once. This mode keeps track of source IDs in memory, which should be fine
  for most use cases. If your dataset is large (10M+ docs), you will likely
  need to parallelize the indexing process regardless.](/python/langchain-core/indexing/api/index)[function

aindex

Async index data from the loader into the vector store.

Indexing functionality uses a manager to keep track of which documents
are in the vector store.

This allows us to keep track of which documents were updated, and which
documents were deleted, which documents should be skipped.

For the time being, documents are indexed using their hashes, and users
are not able to specify the uid of the document.

Behavior changed in `langchain-core` 0.3.25

Added `scoped_full` cleanup mode.

Warning

- In full mode, the loader should be returning
  the entire dataset, and not just a subset of the dataset.
  Otherwise, the auto\_cleanup will remove documents that it is not
  supposed to.
- In incremental mode, if documents associated with a particular
  source id appear across different batches, the indexing API
  will do some redundant work. This will still result in the
  correct end state of the index, but will unfortunately not be
  100% efficient. For example, if a given document is split into 15
  chunks, and we index them using a batch size of 5, we'll have 3 batches
  all with the same source id. In general, to avoid doing too much
  redundant work select as big a batch size as possible.
- The `scoped_full` mode is suitable if determining an appropriate batch size
  is challenging or if your data loader cannot return the entire dataset at
  once. This mode keeps track of source IDs in memory, which should be fine
  for most use cases. If your dataset is large (10M+ docs), you will likely
  need to parallelize the indexing process regardless.](/python/langchain-core/indexing/api/aindex)

## Classes

[class

BaseLoader

Interface for document loader.

Implementations should implement the lazy-loading method using generators to avoid
loading all documents into memory at once.

`load` is provided just for user convenience and should not be overridden.](/python/langchain-core/document_loaders/base/BaseLoader)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

LangChainException

General LangChain exception.](/python/langchain-core/exceptions/LangChainException)[class

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

VectorStore

Interface for vector store.](/python/langchain-core/vectorstores/base/VectorStore)[class

IndexingException

Raised when an indexing operation fails.](/python/langchain-core/indexing/api/IndexingException)[class

IndexingResult

Return a detailed a breakdown of the result of the indexing operation.](/python/langchain-core/indexing/api/IndexingResult)


