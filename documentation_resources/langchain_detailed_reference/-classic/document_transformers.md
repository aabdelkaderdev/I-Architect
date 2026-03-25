<!-- Source: https://reference.langchain.com/python/langchain-classic/document_transformers -->

Modulev1.2.13 (latest)●Since v1.0

# document\_transformers

**Document Transformers** are classes to transform Documents.

**Document Transformers** usually used to transform a lot of Documents in a single run.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/document_transformers/DEPRECATED_LOOKUP)

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

embeddings\_redundant\_filter](/python/langchain-classic/document_transformers/embeddings_redundant_filter)[module

doctran\_text\_translate](/python/langchain-classic/document_transformers/doctran_text_translate)[module

doctran\_text\_qa](/python/langchain-classic/document_transformers/doctran_text_qa)[module

long\_context\_reorder](/python/langchain-classic/document_transformers/long_context_reorder)[module

doctran\_text\_extract](/python/langchain-classic/document_transformers/doctran_text_extract)[module

beautiful\_soup\_transformer](/python/langchain-classic/document_transformers/beautiful_soup_transformer)[module

nuclia\_text\_transform](/python/langchain-classic/document_transformers/nuclia_text_transform)[module

html2text](/python/langchain-classic/document_transformers/html2text)[module

openai\_functions](/python/langchain-classic/document_transformers/openai_functions)[module

google\_translate](/python/langchain-classic/document_transformers/google_translate)


