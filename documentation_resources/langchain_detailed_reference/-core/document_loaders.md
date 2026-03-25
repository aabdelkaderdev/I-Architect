<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders -->

Modulev1.2.21 (latest)●Since v0.1

# document\_loaders

Document loaders.

## Functions

[function

import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.](/python/langchain-core/_import_utils/import_attr)

## Classes

[class

BaseBlobParser

Abstract interface for blob parsers.

A blob parser provides a way to parse raw data stored in a blob into one or more
`Document` objects.

The parser can be composed with blob loaders, making it easy to reuse a parser
independent of how the blob was originally loaded.](/python/langchain-core/document_loaders/base/BaseBlobParser)[class

BaseLoader

Interface for document loader.

Implementations should implement the lazy-loading method using generators to avoid
loading all documents into memory at once.

`load` is provided just for user convenience and should not be overridden.](/python/langchain-core/document_loaders/base/BaseLoader)[class

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
some criteria and return the raw content lazily as a stream of blobs.](/python/langchain-core/document_loaders/blob_loaders/BlobLoader)[class

LangSmithLoader

Load LangSmith Dataset examples as `Document` objects.

Loads the example inputs as the `Document` page content and places the entire
example into the `Document` metadata. This allows you to easily create few-shot
example retrievers from the loaded documents.

Lazy loading

```
from langchain_core.document_loaders import LangSmithLoader

loader = LangSmithLoader(dataset_id="...", limit=100)
docs = []
for doc in loader.lazy_load():
    docs.append(doc)
```

```
# -> [Document("...", metadata={"inputs": {...}, "outputs": {...}, ...}), ...]
```](/python/langchain-core/document_loaders/langsmith/LangSmithLoader)

## Type Aliases

[typeAlias

PathLike](/python/langchain-core/documents/base/PathLike)

## Modules

[module

langsmith

LangSmith document loader.](/python/langchain-core/document_loaders/langsmith)[module

base

Abstract interface for document loader implementations.](/python/langchain-core/document_loaders/base)[module

blob\_loaders

Schema for Blobs and Blob Loaders.

The goal is to facilitate decoupling of content loading from content parsing code. In
addition, content loading code should provide a lazy loading interface by default.](/python/langchain-core/document_loaders/blob_loaders)


