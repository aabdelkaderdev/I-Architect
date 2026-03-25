<!-- Source: https://reference.langchain.com/python/langchain-classic/prompts -->

Modulev1.2.13 (latest)●Since v1.0

# prompts

**Prompt** is the input to the model.

Prompt is often constructed
from multiple components. Prompt classes and functions make constructing and working
with prompts easy.

## Attributes

[attribute

Prompt: PromptTemplate](/python/langchain-classic/prompts/prompt/Prompt)[attribute

MODULE\_LOOKUP: dict](/python/langchain-classic/prompts/MODULE_LOOKUP)

## Functions

[function

create\_importer](/python/langchain-classic/_api/module_import/create_importer)

## Modules



[module

loading](/python/langchain-classic/prompts/loading)

[module

base](/python/langchain-classic/prompts/base)

[module

few\_shot](/python/langchain-classic/prompts/few_shot)

[module

few\_shot\_with\_templates](/python/langchain-classic/prompts/few_shot_with_templates)

[module

prompt](/python/langchain-classic/prompts/prompt)

[module

chat](/python/langchain-classic/prompts/chat)

[module

example\_selector](/python/langchain-classic/prompts/example_selector)

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
loss of type information, IDE support for going to definition etc).

Logic for selecting examples to include in prompts.