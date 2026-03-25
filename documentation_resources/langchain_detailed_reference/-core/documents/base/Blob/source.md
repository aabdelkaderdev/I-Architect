<!-- Source: https://reference.langchain.com/python/langchain-core/documents/base/Blob/source -->

Attributev1.2.21 (latest)●Since v0.2

# source

The source location of the blob as string if known otherwise none.

If a path is associated with the `Blob`, it will default to the path location.

Unless explicitly set via a metadata field called `'source'`, in which
case that value will be used instead.


```
source: str | None
```


