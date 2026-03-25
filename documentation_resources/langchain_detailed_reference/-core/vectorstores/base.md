<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base -->

Modulev1.2.21 (latest)●Since v0.2

# base

A vector store stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.

## Attributes

[attribute

logger](/python/langchain-core/vectorstores/base/logger)[attribute

VST](/python/langchain-core/vectorstores/base/VST)

## Functions

[function

run\_in\_executor

Run a function in an executor.](/python/langchain-core/runnables/config/run_in_executor)

## Classes

[class

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

BaseRetriever

Abstract base class for a document retrieval system.

A retrieval system is defined as something that can take string queries and return
the most 'relevant' documents from some source.

Usage:

A retriever follows the standard `Runnable` interface, and should be used via the
standard `Runnable` methods of `invoke`, `ainvoke`, `batch`, `abatch`.

Implementation:

When implementing a custom retriever, the class should implement the
`_get_relevant_documents` method to define the logic for retrieving documents.

Optionally, an async native implementations can be provided by overriding the
`_aget_relevant_documents` method.

Retriever that returns the first 5 documents from a list of documents

```
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

class SimpleRetriever(BaseRetriever):
    docs: list[Document]
    k: int = 5

    def _get_relevant_documents(self, query: str) -> list[Document]:
        """Return the first k documents from the list of documents"""
        return self.docs[:self.k]

    async def _aget_relevant_documents(self, query: str) -> list[Document]:
        """(Optional) async native implementation."""
        return self.docs[:self.k]
```

Simple retriever based on a scikit-learn vectorizer

```
from sklearn.metrics.pairwise import cosine_similarity

class TFIDFRetriever(BaseRetriever, BaseModel):
    vectorizer: Any
    docs: list[Document]
    tfidf_array: Any
    k: int = 4

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> list[Document]:
        # Ip -- (n_docs,x), Op -- (n_docs,n_Feats)
        query_vec = self.vectorizer.transform([query])
        # Op -- (n_docs,1) -- Cosine Sim with each doc
        results = cosine_similarity(self.tfidf_array, query_vec).reshape((-1,))
        return [self.docs[i] for i in results.argsort()[-self.k :][::-1]]
```](/python/langchain-core/retrievers/BaseRetriever)[class

LangSmithRetrieverParams

LangSmith parameters for tracing.](/python/langchain-core/retrievers/LangSmithRetrieverParams)[class

AsyncCallbackManagerForRetrieverRun

Async callback manager for retriever run.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForRetrieverRun)[class

CallbackManagerForRetrieverRun

Callback manager for retriever run.](/python/langchain-core/callbacks/manager/CallbackManagerForRetrieverRun)[class

VectorStore

Interface for vector store.](/python/langchain-core/vectorstores/base/VectorStore)[class

VectorStoreRetriever

Base Retriever class for VectorStore.](/python/langchain-core/vectorstores/base/VectorStoreRetriever)


