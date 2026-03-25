<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/base/DeleteResponse/succeeded -->

Attributev1.2.21 (latest)●Since v0.2

# succeeded

The IDs that were successfully deleted.

If returned, this should only include *actual* deletions.

If the ID did not exist to begin with,
it should not be included in this list.


```
succeeded: Sequence[str]
```


