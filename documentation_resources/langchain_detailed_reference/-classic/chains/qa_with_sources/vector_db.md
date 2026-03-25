<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/vector_db -->

Modulev1.2.13 (latest)●Since v1.0

# vector\_db

Question-answering with sources over a vector database.

## Classes

[class

VectorDBQAWithSourcesChain

Question-answering with sources over a vector database.](/python/langchain-classic/chains/qa_with_sources/vector_db/VectorDBQAWithSourcesChain)[deprecatedclass

StuffDocumentsChain

Chain that combines documents by stuffing into context.

This chain takes a list of documents and first combines them into a single string.
It does this by formatting each document into a string with the `document_prompt`
and then joining them together with `document_separator`. It then adds that new
string to the inputs with the variable name set by `document_variable_name`.
Those inputs are then passed to the `llm_chain`.](/python/langchain-classic/chains/combine_documents/stuff/StuffDocumentsChain)[deprecatedclass

BaseQAWithSourcesChain

Question answering chain with sources over documents.](/python/langchain-classic/chains/qa_with_sources/base/BaseQAWithSourcesChain)


