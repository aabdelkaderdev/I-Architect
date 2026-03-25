<!-- Source: https://reference.langchain.com/python/langchain-classic/graphs -->

Modulev1.2.13 (latest)●Since v1.0

# graphs

**Graphs** provide a natural language interface to graph databases.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/graphs/DEPRECATED_LOOKUP)

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

## Modules

[module

hugegraph](/python/langchain-classic/graphs/hugegraph)[module

arangodb\_graph](/python/langchain-classic/graphs/arangodb_graph)[module

rdf\_graph](/python/langchain-classic/graphs/rdf_graph)[module

graph\_document](/python/langchain-classic/graphs/graph_document)[module

falkordb\_graph](/python/langchain-classic/graphs/falkordb_graph)[module

networkx\_graph](/python/langchain-classic/graphs/networkx_graph)[module

nebula\_graph](/python/langchain-classic/graphs/nebula_graph)[module

neptune\_graph](/python/langchain-classic/graphs/neptune_graph)[module

memgraph\_graph](/python/langchain-classic/graphs/memgraph_graph)[module

neo4j\_graph](/python/langchain-classic/graphs/neo4j_graph)[module

graph\_store](/python/langchain-classic/graphs/graph_store)[module

kuzu\_graph](/python/langchain-classic/graphs/kuzu_graph)


