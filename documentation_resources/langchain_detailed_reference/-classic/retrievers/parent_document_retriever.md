<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever -->

Modulev1.2.13 (latest)●Since v1.0

# parent\_document\_retriever

## Classes

[class

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
while preserving full document context.](/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever)[class

ParentDocumentRetriever

Retrieve small chunks then retrieve their parent documents.

When splitting documents for retrieval, there are often conflicting desires:

1. You may want to have small documents, so that their embeddings can most
   accurately reflect their meaning. If too long, then the embeddings can
   lose meaning.
2. You want to have long enough documents that the context of each chunk is
   retained.

The ParentDocumentRetriever strikes that balance by splitting and storing
small chunks of data. During retrieval, it first fetches the small chunks
but then looks up the parent IDs for those chunks and returns those larger
documents.

Note that "parent document" refers to the document that a small chunk
originated from. This can either be the whole raw document OR a larger
chunk.](/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever)


