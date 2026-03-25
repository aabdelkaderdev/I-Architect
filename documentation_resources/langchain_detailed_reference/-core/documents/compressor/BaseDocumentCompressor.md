<!-- Source: https://reference.langchain.com/python/langchain-core/documents/compressor/BaseDocumentCompressor -->

Classv1.2.21 (latest)●Since v0.1

# BaseDocumentCompressor

Base class for document compressors.

This abstraction is primarily used for post-processing of retrieved documents.

`Document` objects matching a given query are first retrieved.

Then the list of documents can be further processed.

For example, one could re-rank the retrieved documents using an LLM.

Note

Users should favor using a `RunnableLambda` instead of sub-classing from this
interface.


```
BaseDocumentCompressor()
```

## Bases

`BaseModel``ABC`

## Methods

[method

compress\_documents

Compress retrieved documents given the query context.](/python/langchain-core/documents/compressor/BaseDocumentCompressor/compress_documents)[method

acompress\_documents

Async compress retrieved documents given the query context.](/python/langchain-core/documents/compressor/BaseDocumentCompressor/acompress_documents)


