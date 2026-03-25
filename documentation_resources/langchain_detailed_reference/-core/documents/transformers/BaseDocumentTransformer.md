<!-- Source: https://reference.langchain.com/python/langchain-core/documents/transformers/BaseDocumentTransformer -->

Classv1.2.21 (latest)●Since v0.1

# BaseDocumentTransformer

Abstract base class for document transformation.

A document transformation takes a sequence of `Document` objects and returns a
sequence of transformed `Document` objects.


```
BaseDocumentTransformer()
```

## Bases

`ABC`

**Example:**

```
class EmbeddingsRedundantFilter(BaseDocumentTransformer, BaseModel):
    embeddings: Embeddings
    similarity_fn: Callable = cosine_similarity
    similarity_threshold: float = 0.95

    class Config:
        arbitrary_types_allowed = True

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        stateful_documents = get_stateful_documents(documents)
        embedded_documents = _get_embeddings_from_stateful_docs(
            self.embeddings, stateful_documents
        )
        included_idxs = _filter_similar_embeddings(
            embedded_documents,
            self.similarity_fn,
            self.similarity_threshold,
        )
        return [stateful_documents[i] for i in sorted(included_idxs)]

    async def atransform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        raise NotImplementedError
```

## Methods

[method

transform\_documents

Transform a list of documents.](/python/langchain-core/documents/transformers/BaseDocumentTransformer/transform_documents)[method

atransform\_documents

Asynchronously transform a list of documents.](/python/langchain-core/documents/transformers/BaseDocumentTransformer/atransform_documents)


