<!-- Source: https://reference.langchain.com/python/langchain-core/example_selectors/semantic_similarity -->

Modulev1.2.21 (latest)●Since v0.1

# semantic\_similarity

Example selector that selects examples based on SemanticSimilarity.

## Functions

[function

sorted\_values

Return a list of values in dict sorted by key.](/python/langchain-core/example_selectors/semantic_similarity/sorted_values)

## Classes

[class

BaseExampleSelector

Interface for selecting examples to include in prompts.](/python/langchain-core/example_selectors/base/BaseExampleSelector)[class

VectorStore

Interface for vector store.](/python/langchain-core/vectorstores/base/VectorStore)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

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

SemanticSimilarityExampleSelector

Select examples based on semantic similarity.](/python/langchain-core/example_selectors/semantic_similarity/SemanticSimilarityExampleSelector)[class

MaxMarginalRelevanceExampleSelector

Select examples based on Max Marginal Relevance.

This was shown to improve performance in this paper:
<https://arxiv.org/pdf/2211.13892.pdf>](/python/langchain-core/example_selectors/semantic_similarity/MaxMarginalRelevanceExampleSelector)


