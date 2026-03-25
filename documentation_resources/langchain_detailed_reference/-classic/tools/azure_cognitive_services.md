<!-- Source: https://reference.langchain.com/python/langchain-classic/tools/azure_cognitive_services -->

Modulev1.2.13 (latest)●Since v1.0

# azure\_cognitive\_services

Azure Cognitive Services Tools.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/tools/azure_cognitive_services/DEPRECATED_LOOKUP)

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

speech2text](/python/langchain-classic/tools/azure_cognitive_services/speech2text)[module

form\_recognizer](/python/langchain-classic/tools/azure_cognitive_services/form_recognizer)[module

text\_analytics\_health](/python/langchain-classic/tools/azure_cognitive_services/text_analytics_health)[module

text2speech](/python/langchain-classic/tools/azure_cognitive_services/text2speech)[module

image\_analysis](/python/langchain-classic/tools/azure_cognitive_services/image_analysis)


