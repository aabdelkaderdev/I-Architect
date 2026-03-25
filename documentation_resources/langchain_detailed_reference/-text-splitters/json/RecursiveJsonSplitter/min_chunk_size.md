<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/json/RecursiveJsonSplitter/min_chunk_size -->

Attributev1.1.1 (latest)●Since v0.0

# min\_chunk\_size

The minimum size for each chunk, derived from `max_chunk_size` if not
explicitly provided.


```
min_chunk_size: int = min_chunk_size if min_chunk_size is not None else max(
  max_chunk_size  200,
  50
)
```


