<!-- Source: https://reference.langchain.com/python/langchain-core/documents/compressor -->

Modulev1.2.21 (latest)●Since v0.1

# compressor

Document compressor.

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

BaseDocumentCompressor

Base class for document compressors.

This abstraction is primarily used for post-processing of retrieved documents.

`Document` objects matching a given query are first retrieved.

Then the list of documents can be further processed.

For example, one could re-rank the retrieved documents using an LLM.

Note

Users should favor using a `RunnableLambda` instead of sub-classing from this
interface.](/python/langchain-core/documents/compressor/BaseDocumentCompressor)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


