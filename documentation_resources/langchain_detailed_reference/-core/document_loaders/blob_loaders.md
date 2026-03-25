<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/blob_loaders -->

Modulev1.2.21 (latest)●Since v0.1

# blob\_loaders

Schema for Blobs and Blob Loaders.

The goal is to facilitate decoupling of content loading from content parsing code. In
addition, content loading code should provide a lazy loading interface by default.

## Classes

[class

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

BlobLoader

Abstract interface for blob loaders implementation.

Implementer should be able to load raw content from a storage system according to
some criteria and return the raw content lazily as a stream of blobs.](/python/langchain-core/document_loaders/blob_loaders/BlobLoader)

## Type Aliases

[typeAlias

PathLike](/python/langchain-core/documents/base/PathLike)


