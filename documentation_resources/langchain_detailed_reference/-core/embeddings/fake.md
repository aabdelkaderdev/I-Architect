<!-- Source: https://reference.langchain.com/python/langchain-core/embeddings/fake -->

Modulev1.2.21 (latest)●Since v0.1

# fake

Module contains a few fake embedding models for testing purposes.

## Classes

[class

Embeddings

Interface for embedding models.

This is an interface meant for implementing text embedding models.

Text embedding models are used to map text to a vector (a point in n-dimensional
space).

Texts that are similar will usually be mapped to points that are close to each
other in this space. The exact details of what's considered "similar" and how
"distance" is measured in this space are dependent on the specific embedding model.

This abstraction contains a method for embedding a list of documents and a method
for embedding a query text. The embedding of a query text is expected to be a single
vector, while the embedding of a list of documents is expected to be a list of
vectors.

Usually the query embedding is identical to the document embedding, but the
abstraction allows treating them independently.

In addition to the synchronous methods, this interface also provides asynchronous
versions of the methods.

By default, the asynchronous methods are implemented using the synchronous methods;
however, implementations may choose to override the asynchronous methods with
an async native implementation for performance reasons.](/python/langchain-core/embeddings/embeddings/Embeddings)[class

FakeEmbeddings

Fake embedding model for unit testing purposes.

This embedding model creates embeddings by sampling from a normal distribution.

Toy model

Do not use this outside of testing, as it is not a real embedding model.](/python/langchain-core/embeddings/fake/FakeEmbeddings)[class

DeterministicFakeEmbedding

Deterministic fake embedding model for unit testing purposes.

This embedding model creates embeddings by sampling from a normal distribution
with a seed based on the hash of the text.

Toy model

Do not use this outside of testing, as it is not a real embedding model.](/python/langchain-core/embeddings/fake/DeterministicFakeEmbedding)


