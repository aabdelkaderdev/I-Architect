<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/api/IndexingResult -->

Classv1.2.21 (latest)●Since v0.1

# IndexingResult

Return a detailed a breakdown of the result of the indexing operation.


```
IndexingResult()
```

## Bases

`TypedDict`

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| num\_added | [int](https://docs.python.org/3/library/functions.html#int) |
| num\_updated | [int](https://docs.python.org/3/library/functions.html#int) |
| num\_deleted | [int](https://docs.python.org/3/library/functions.html#int) |
| num\_skipped | [int](https://docs.python.org/3/library/functions.html#int) |

## Attributes

[attribute

num\_added: int

Number of added documents.](/python/langchain-core/indexing/api/IndexingResult/num_added)[attribute

num\_updated: int

Number of updated documents because they were not up to date.](/python/langchain-core/indexing/api/IndexingResult/num_updated)[attribute

num\_deleted: int

Number of deleted documents.](/python/langchain-core/indexing/api/IndexingResult/num_deleted)[attribute

num\_skipped: int

Number of skipped documents because they were already up to date.](/python/langchain-core/indexing/api/IndexingResult/num_skipped)


