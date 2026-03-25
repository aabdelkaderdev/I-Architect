<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank -->

Classv1.2.13 (latest)●Since v1.0

# LLMListwiseRerank


```
LLMListwiseRerank()
```

## Bases

`BaseDocumentCompressor`

## Attributes

## Methods

## Inherited from[BaseDocumentCompressor](/python/langchain-core/documents/compressor/BaseDocumentCompressor)(langchain\_core)

### Methods

[Macompress\_documents](/python/langchain-core/documents/compressor/BaseDocumentCompressor/acompress_documents)



[attribute

reranker: Runnable[dict, list[Document]]

LLM-based reranker to use for filtering documents. Expected to take in a dict
with 'documents: Sequence[Document]' and 'query: str' keys and output a
List[Document].](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/reranker)

[attribute

top\_n: int

Number of documents to return.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/top_n)

[attribute

model\_config](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/model_config)

[method

compress\_documents

Filter down documents based on their relevance to the query.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/compress_documents)

[method

from\_llm

Create a LLMListwiseRerank document compressor from a language model.](/python/langchain-classic/retrievers/document_compressors/listwise_rerank/LLMListwiseRerank/from_llm)

Document compressor that uses `Zero-Shot Listwise Document Reranking`.

Adapted from: <https://arxiv.org/pdf/2305.02156.pdf>

`LLMListwiseRerank` uses a language model to rerank a list of documents based on
their relevance to a query.

Note

Requires that underlying model implement `with_structured_output`.

**Example usage:**

```
from langchain_classic.retrievers.document_compressors.listwise_rerank import (
    LLMListwiseRerank,
)
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

documents = [
    Document("Sally is my friend from school"),
    Document("Steve is my friend from home"),
    Document("I didn't always like yogurt"),
    Document("I wonder why it's called football"),
    Document("Where's waldo"),
]

reranker = LLMListwiseRerank.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"), top_n=3
)
compressed_docs = reranker.compress_documents(documents, "Who is steve")
assert len(compressed_docs) == 3
assert "Steve" in compressed_docs[0].page_content
```