<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/base/BaseLoader -->

Classv1.2.21 (latest)●Since v0.1

# BaseLoader

Interface for document loader.

Implementations should implement the lazy-loading method using generators to avoid
loading all documents into memory at once.

`load` is provided just for user convenience and should not be overridden.


```
BaseLoader()
```

## Bases

`ABC`

## Methods

[method

load

Load data into `Document` objects.](/python/langchain-core/document_loaders/base/BaseLoader/load)[method

aload

Load data into `Document` objects.](/python/langchain-core/document_loaders/base/BaseLoader/aload)[method

load\_and\_split

Load `Document` and split into chunks. Chunks are returned as `Document`.

Danger

Do not override this method. It should be considered to be deprecated!](/python/langchain-core/document_loaders/base/BaseLoader/load_and_split)[method

lazy\_load

A lazy loader for `Document`.](/python/langchain-core/document_loaders/base/BaseLoader/lazy_load)[method

alazy\_load

A lazy loader for `Document`.](/python/langchain-core/document_loaders/base/BaseLoader/alazy_load)


