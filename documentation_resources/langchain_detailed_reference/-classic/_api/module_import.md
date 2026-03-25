<!-- Source: https://reference.langchain.com/python/langchain-classic/_api/module_import -->

Modulev1.2.13 (latest)●Since v1.0

# module\_import

## Attributes

[attribute

ALLOWED\_TOP\_LEVEL\_PKGS: set](/python/langchain-classic/_api/module_import/ALLOWED_TOP_LEVEL_PKGS)

## Functions

[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-classic/_api/interactive_env/is_interactive_env)[function

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


