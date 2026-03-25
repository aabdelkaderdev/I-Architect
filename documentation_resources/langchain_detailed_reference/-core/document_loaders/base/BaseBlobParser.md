<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/base/BaseBlobParser -->

Classv1.2.21 (latest)●Since v0.1

# BaseBlobParser

Abstract interface for blob parsers.

A blob parser provides a way to parse raw data stored in a blob into one or more
`Document` objects.

The parser can be composed with blob loaders, making it easy to reuse a parser
independent of how the blob was originally loaded.


```
BaseBlobParser()
```

## Bases

`ABC`

## Methods

[method

lazy\_parse

Lazy parsing interface.

Subclasses are required to implement this method.](/python/langchain-core/document_loaders/base/BaseBlobParser/lazy_parse)[method

parse

Eagerly parse the blob into a `Document` or list of `Document` objects.

This is a convenience method for interactive development environment.

Production applications should favor the `lazy_parse` method instead.

Subclasses should generally not over-ride this parse method.](/python/langchain-core/document_loaders/base/BaseBlobParser/parse)


