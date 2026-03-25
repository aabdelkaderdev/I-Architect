<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/base -->

Modulev1.2.21 (latest)●Since v0.1

# base

Abstract interface for document loader implementations.

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

Blob

Raw data abstraction for document loading and file processing.

Represents raw bytes or text, either in-memory or by file reference. Used
primarily by document loaders to decouple data loading from parsing.

Inspired by [Mozilla's `Blob`](https://developer.mozilla.org/en-US/docs/Web/API/Blob)

Initialize a blob from in-memory data

```
from langchain_core.documents import Blob

blob = Blob.from_data("Hello, world!")

# Read the blob as a string
print(blob.as_string())

# Read the blob as bytes
print(blob.as_bytes())

# Read the blob as a byte stream
with blob.as_bytes_io() as f:
    print(f.read())
```

Load from memory and specify MIME type and metadata

```
from langchain_core.documents import Blob

blob = Blob.from_data(
    data="Hello, world!",
    mime_type="text/plain",
    metadata={"source": "https://example.com"},
)
```

Load the blob from a file

```
from langchain_core.documents import Blob

blob = Blob.from_path("path/to/file.txt")

# Read the blob as a string
print(blob.as_string())

# Read the blob as bytes
print(blob.as_bytes())

# Read the blob as a byte stream
with blob.as_bytes_io() as f:
    print(f.read())
```](/python/langchain-core/documents/base/Blob)[class

BaseLoader

Interface for document loader.

Implementations should implement the lazy-loading method using generators to avoid
loading all documents into memory at once.

`load` is provided just for user convenience and should not be overridden.](/python/langchain-core/document_loaders/base/BaseLoader)[class

BaseBlobParser

Abstract interface for blob parsers.

A blob parser provides a way to parse raw data stored in a blob into one or more
`Document` objects.

The parser can be composed with blob loaders, making it easy to reuse a parser
independent of how the blob was originally loaded.](/python/langchain-core/document_loaders/base/BaseBlobParser)


