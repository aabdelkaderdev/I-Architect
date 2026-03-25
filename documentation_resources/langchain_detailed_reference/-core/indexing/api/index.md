<!-- Source: https://reference.langchain.com/python/langchain-core/indexing/api/index -->

Functionv1.2.21 (latest)●Since v0.1

# index

Index data from the loader into the vector store.

Indexing functionality uses a manager to keep track of which documents
are in the vector store.

This allows us to keep track of which documents were updated, and which
documents were deleted, which documents should be skipped.

For the time being, documents are indexed using their hashes, and users
are not able to specify the uid of the document.

Behavior changed in `langchain-core` 0.3.25

Added `scoped_full` cleanup mode.

Warning

- In full mode, the loader should be returning
  the entire dataset, and not just a subset of the dataset.
  Otherwise, the auto\_cleanup will remove documents that it is not
  supposed to.
- In incremental mode, if documents associated with a particular
  source id appear across different batches, the indexing API
  will do some redundant work. This will still result in the
  correct end state of the index, but will unfortunately not be
  100% efficient. For example, if a given document is split into 15
  chunks, and we index them using a batch size of 5, we'll have 3 batches
  all with the same source id. In general, to avoid doing too much
  redundant work select as big a batch size as possible.
- The `scoped_full` mode is suitable if determining an appropriate batch size
  is challenging or if your data loader cannot return the entire dataset at
  once. This mode keeps track of source IDs in memory, which should be fine
  for most use cases. If your dataset is large (10M+ docs), you will likely
  need to parallelize the indexing process regardless.


```
index(
  docs_source: BaseLoader | Iterable[Document],
  record_manager: RecordManager,
  vector_store: VectorStore | DocumentIndex,
  *,
  batch_size: int = 100,
  cleanup: Literal['incremental', 'full', 'scoped_full'] | None = None,
  source_id_key: str | Callable[[Document], str] | None = None,
  cleanup_batch_size: int = 1000,
  force_update: bool = False,
  key_encoder: Literal['sha1', 'sha256', 'sha512', 'blake2b'] | Callable[[Document], str] = 'sha1',
  upsert_kwargs: dict[str, Any] | None = None
) -> IndexingResult
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `docs_source`\* | `BaseLoader | Iterable[Document]` | Data loader or iterable of documents to index. |
| `record_manager`\* | `RecordManager` | Timestamped set to keep track of which documents were updated. |
| `vector_store`\* | `VectorStore | DocumentIndex` | `VectorStore` or DocumentIndex to index the documents into. |
| `batch_size` | `int` | Default:`100`  Batch size to use when indexing. |
| `cleanup` | `Literal['incremental', 'full', 'scoped_full'] | None` | Default:`None`  How to handle clean up of documents.   - incremental: Cleans up all documents that haven't been updated AND   that are associated with source IDs that were seen during indexing.   Clean up is done continuously during indexing helping to minimize the   probability of users seeing duplicated content. - full: Delete all documents that have not been returned by the loader   during this run of indexing.   Clean up runs after all documents have been indexed.   This means that users may see duplicated content during indexing. - scoped\_full: Similar to Full, but only deletes all documents   that haven't been updated AND that are associated with   source IDs that were seen during indexing. - None: Do not delete any documents. |
| `source_id_key` | `str | Callable[[Document], str] | None` | Default:`None`  Optional key that helps identify the original source of the document. |
| `cleanup_batch_size` | `int` | Default:`1000`  Batch size to use when cleaning up documents. |
| `force_update` | `bool` | Default:`False`  Force update documents even if they are present in the record manager. Useful if you are re-indexing with updated embeddings. |
| `key_encoder` | `Literal['sha1', 'sha256', 'sha512', 'blake2b'] | Callable[[Document], str]` | Default:`'sha1'`  Hashing algorithm to use for hashing the document content and metadata. Options include "blake2b", "sha256", and "sha512". |
| `key_encoder` | `Literal['sha1', 'sha256', 'sha512', 'blake2b'] | Callable[[Document], str]` | Default:`'sha1'`  Hashing algorithm to use for hashing the document. If not provided, a default encoder using SHA-1 will be used. SHA-1 is not collision-resistant, and a motivated attacker could craft two different texts that hash to the same cache key.  New applications should use one of the alternative encoders or provide a custom and strong key encoder function to avoid this risk.  When changing the key encoder, you must change the index as well to avoid duplicated documents in the cache. |
| `upsert_kwargs` | `dict[str, Any] | None` | Default:`None`  Additional keyword arguments to pass to the add\_documents method of the `VectorStore` or the upsert method of the DocumentIndex. For example, you can use this to specify a custom vector\_field: upsert\_kwargs={"vector\_field": "embedding"} |


