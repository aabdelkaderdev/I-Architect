<!-- Source: https://reference.langchain.com/python/langchain-classic/document_loaders/parsers/audio -->

Modulev1.2.13 (latest)●Since v1.0

# audio

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/document_loaders/parsers/audio/DEPRECATED_LOOKUP)

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


