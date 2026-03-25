<!-- Source: https://reference.langchain.com/python/langchain-classic/tools/playwright -->

Modulev1.2.13 (latest)●Since v1.0

# playwright

Browser tools and toolkit.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/tools/playwright/DEPRECATED_LOOKUP)

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

base](/python/langchain-classic/tools/playwright/base)[module

extract\_hyperlinks](/python/langchain-classic/tools/playwright/extract_hyperlinks)[module

navigate\_back](/python/langchain-classic/tools/playwright/navigate_back)[module

current\_page](/python/langchain-classic/tools/playwright/current_page)[module

get\_elements](/python/langchain-classic/tools/playwright/get_elements)[module

extract\_text](/python/langchain-classic/tools/playwright/extract_text)[module

navigate](/python/langchain-classic/tools/playwright/navigate)[module

click](/python/langchain-classic/tools/playwright/click)


