<!-- Source: https://reference.langchain.com/python/langchain-classic/docstore -->

Modulev1.2.13 (latest)●Since v1.0

# docstore

**Docstores** are classes to store and load Documents.

The **Docstore** is a simplified version of the Document Loader.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/docstore/DEPRECATED_LOOKUP)

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

in\_memory](/python/langchain-classic/docstore/in_memory)[module

base](/python/langchain-classic/docstore/base)[module

document](/python/langchain-classic/docstore/document)[module

arbitrary\_fn](/python/langchain-classic/docstore/arbitrary_fn)[module

wikipedia](/python/langchain-classic/docstore/wikipedia)


