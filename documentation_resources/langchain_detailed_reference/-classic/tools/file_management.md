<!-- Source: https://reference.langchain.com/python/langchain-classic/tools/file_management -->

Modulev1.2.13 (latest)●Since v1.0

# file\_management

File Management Tools.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/tools/file_management/DEPRECATED_LOOKUP)

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

file\_search](/python/langchain-classic/tools/file_management/file_search)[module

delete](/python/langchain-classic/tools/file_management/delete)[module

move](/python/langchain-classic/tools/file_management/move)[module

list\_dir](/python/langchain-classic/tools/file_management/list_dir)[module

write](/python/langchain-classic/tools/file_management/write)[module

read](/python/langchain-classic/tools/file_management/read)[module

copy](/python/langchain-classic/tools/file_management/copy)


