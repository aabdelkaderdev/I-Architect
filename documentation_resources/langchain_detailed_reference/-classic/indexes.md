<!-- Source: https://reference.langchain.com/python/langchain-classic/indexes -->

Modulev1.2.13 (latest)●Since v1.0

# indexes

**Indexes**.

**Index** is used to avoid writing duplicated content
into the vectostore and to avoid over-writing content if it's unchanged.

Indexes also :

- Create knowledge graphs from data.
- Support indexing workflows from LangChain data loaders to vectorstores.

Importantly, Index keeps on working even if the content being written is derived
via a set of transformations from some source content (e.g., indexing children
documents that were derived from parent documents by chunking.)

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/indexes/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Classes

[class

SQLRecordManager

A SQL Alchemy based implementation of the record manager.](/python/langchain-classic/indexes/_sql_record_manager/SQLRecordManager)[class

VectorstoreIndexCreator

Logic for creating indexes.](/python/langchain-classic/indexes/vectorstore/VectorstoreIndexCreator)

## Modules

[module

graph

**Graphs** provide a natural language interface to graph databases.](/python/langchain-classic/indexes/graph)[module

vectorstore

Vectorstore stubs for the indexing api.](/python/langchain-classic/indexes/vectorstore)[module

prompts

Relevant prompts for constructing indexes.](/python/langchain-classic/indexes/prompts)


