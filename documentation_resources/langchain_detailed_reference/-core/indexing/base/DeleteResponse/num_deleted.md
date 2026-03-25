<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DeleteResponse/num_deleted -->

Attributev1.2.21 (latest)●Since v0.2

# num\_deleted

The number of items that were successfully deleted.

If returned, this should only include *actual* deletions.

If the ID did not exist to begin with,
it should not be included in this count.


```
num_deleted: int
```


