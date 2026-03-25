<!-- Source: https://reference.langchain.com/python/langchain-classic/utils -->

Modulev1.2.13 (latest)●Since v1.0

# utils

Utility functions for LangChain.

These functions do not depend on any other LangChain module.

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

math](/python/langchain-classic/utils/math)[module

json\_schema](/python/langchain-classic/utils/json_schema)[module

html](/python/langchain-classic/utils/html)[module

utils](/python/langchain-classic/utils/utils)[module

input](/python/langchain-classic/utils/input)[module

aiter](/python/langchain-classic/utils/aiter)[module

openai](/python/langchain-classic/utils/openai)[module

iter](/python/langchain-classic/utils/iter)[module

formatting](/python/langchain-classic/utils/formatting)[module

strings](/python/langchain-classic/utils/strings)[module

ernie\_functions](/python/langchain-classic/utils/ernie_functions)[module

env](/python/langchain-classic/utils/env)[module

pydantic](/python/langchain-classic/utils/pydantic)[module

openai\_functions](/python/langchain-classic/utils/openai_functions)


