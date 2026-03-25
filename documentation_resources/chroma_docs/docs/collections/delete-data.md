<!-- Source: https://docs.trychroma.com/docs/collections/delete-data -->

Chroma supports deleting items from a collection by `id` using `.delete`. The embeddings, documents, and metadata associated with each item will be deleted.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.delete(
    ids=["id1", "id2", "id3",...],
)
```

`.delete` also supports the `where` filter. It will delete all items in the collection that match the `where` filter.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.delete(
	where={"chapter": "20"}
)
```