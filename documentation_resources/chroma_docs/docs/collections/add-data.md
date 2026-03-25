<!-- Source: https://docs.trychroma.com/docs/collections/add-data -->

## [​](#adding-data) Adding Data

Use `.add` to insert new records into a collection. Each record needs a unique string `id`.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.add(
    ids=["id1", "id2", "id3"],
    documents=["lorem ipsum...", "doc2", "doc3"],
    metadatas=[{"chapter": 3, "verse": 16}, {"chapter": 3, "verse": 5}, {"chapter": 29, "verse": 11}],
)
```

You must provide either `documents`, `embeddings`, or both. `metadatas` are always optional.
When only providing `documents`, Chroma will generate embeddings for you using the collection’s [embedding function](/docs/embeddings/embedding-functions).
If you’ve already computed embeddings, pass them alongside `documents`. Chroma will store both as-is without re-embedding the documents.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.add(
    ids=["id1", "id2", "id3"],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2]],
    documents=["doc1", "doc2", "doc3"],
    metadatas=[{"chapter": 3, "verse": 16}, {"chapter": 3, "verse": 5}, {"chapter": 29, "verse": 11}],
)
```

If your documents are stored elsewhere, you can add just embeddings and metadata. Use the `ids` to associate records with your external documents.
This is a useful pattern if your documents are very large, such as high-resolution
images or videos.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.add(
    ids=["id1", "id2", "id3"],
    embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2]],
    metadatas=[{"chapter": 3, "verse": 16}, {"chapter": 3, "verse": 5}, {"chapter": 29, "verse": 11}],
)
```

## [​](#metadata) Metadata

Metadata values can be strings, integers, floats, or booleans. Additionally, you can store arrays of these types.

Python

TypeScript

Rust

Report incorrect code

Copy

Ask AI

```
collection.add(
    ids=["id1"],
    documents=["lorem ipsum..."],
    metadatas=[{
        "chapter": 3,
        "tags": ["fiction", "adventure"],
        "scores": [1, 2, 3],
    }],
)
```

All elements in an array must be the same type, and empty arrays are not allowed. You can filter on array metadata using the `$contains` and `$not_contains` operators — see [Metadata Filtering](/docs/querying-collections/metadata-filtering#using-array-metadata) for details.

## [​](#behaviors) Behaviors

- If you add a record with an ID that already exists in the collection, it will be ignored without throwing an error. In order to overwrite data in your collection, you must [update](./update-data) the data.
- If the supplied embeddings don’t match the dimensionality of embeddings already in the collection, an exception will be raised.