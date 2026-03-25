<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/blob_loaders/BlobLoader -->

Classv1.2.21 (latest)●Since v0.1

# BlobLoader

Abstract interface for blob loaders implementation.

Implementer should be able to load raw content from a storage system according to
some criteria and return the raw content lazily as a stream of blobs.


```
BlobLoader()
```

## Bases

`ABC`

## Methods

[method

yield\_blobs

A lazy loader for raw data represented by LangChain's `Blob` object.](/python/langchain-core/document_loaders/blob_loaders/BlobLoader/yield_blobs)


