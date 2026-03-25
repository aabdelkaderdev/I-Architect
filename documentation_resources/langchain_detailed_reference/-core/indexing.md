<!-- Source: https://reference.langchain.com/python/langchain-core/indexing -->

Modulev1.2.21 (latest)●Since v0.1

# indexing

Code to help indexing data into a vectorstore.

This package contains helper logic to help deal with indexing data into
a `VectorStore` while avoiding duplicated content and over-writing content
if it's unchanged.

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)[function

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
  need to parallelize the indexing process regardless.](/python/langchain-core/indexing/api/aindex)[function

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
  need to parallelize the indexing process regardless.](/python/langchain-core/indexing/api/index)

## Classes

[class

IndexingResult

Return a detailed a breakdown of the result of the indexing operation.](/python/langchain-core/indexing/api/IndexingResult)[class

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

InMemoryRecordManager

An in-memory record manager for testing purposes.](/python/langchain-core/indexing/base/InMemoryRecordManager)[class

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
indexed to avoid this issue.](/python/langchain-core/indexing/base/UpsertResponse)

## Modules

[module

in\_memory

In memory document index.](/python/langchain-core/indexing/in_memory)[module

base

Base classes for indexing.](/python/langchain-core/indexing/base)[module

api

Module contains logic for indexing documents into vector stores.](/python/langchain-core/indexing/api)


