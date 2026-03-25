<!-- Source: https://reference.langchain.com/python/langchain-core/documents/transformers -->

Modulev1.2.21 (latest)●Since v0.1

# transformers

Document transformers.

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

BaseDocumentTransformer

Abstract base class for document transformation.

A document transformation takes a sequence of `Document` objects and returns a
sequence of transformed `Document` objects.](/python/langchain-core/documents/transformers/BaseDocumentTransformer)


