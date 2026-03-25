<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_vector -->

Modulev1.2.13 (latest)●Since v1.0

# multi\_vector

## Functions

[function

create\_kv\_docstore

Create a store for langchain `Document` objects from a bytes store.

This store does run time type checking to ensure that the values are
`Document` objects.](/python/langchain-classic/storage/_lc_store/create_kv_docstore)

## Classes

[class

SearchType

Enumerator of the types of search to perform.](/python/langchain-classic/retrievers/multi_vector/SearchType)[class

MultiVectorRetriever

Retriever that supports multiple embeddings per parent document.

This retriever is designed for scenarios where documents are split into
smaller chunks for embedding and vector search, but retrieval returns
the original parent documents rather than individual chunks.

It works by:

- Performing similarity (or MMR) search over embedded child chunks
- Collecting unique parent document IDs from chunk metadata
- Fetching and returning the corresponding parent documents from the docstore

This pattern is commonly used in RAG pipelines to improve answer grounding
while preserving full document context.](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever)


