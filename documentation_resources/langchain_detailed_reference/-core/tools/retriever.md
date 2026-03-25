<!-- Source: https://reference.langchain.com/python/langchain-core/tools/retriever -->

Modulev1.2.21 (latest)●Since v0.2

# retriever

Retriever tool.

## Functions

[function

aformat\_document

Async format a document into a string based on a prompt template.

First, this pulls information from the document from two sources:

1. `page_content`: This takes the information from the `document.page_content` and
   assigns it to a variable named `page_content`.
2. `metadata`: This takes information from `document.metadata` and assigns it to
   variables of the same name.

Those variables are then passed into the `prompt` to produce a formatted string.](/python/langchain-core/prompts/base/aformat_document)[function

format\_document

Format a document into a string based on a prompt template.

First, this pulls information from the document from two sources:

1. `page_content`: This takes the information from the `document.page_content` and
   assigns it to a variable named `page_content`.
2. `metadata`: This takes information from `document.metadata` and assigns it to
   variables of the same name.

Those variables are then passed into the `prompt` to produce a formatted string.](/python/langchain-core/prompts/base/format_document)[function

create\_retriever\_tool

Create a tool to do retrieval of documents.](/python/langchain-core/tools/retriever/create_retriever_tool)

## Classes

[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

BasePromptTemplate

Base class for all prompt templates, returning a prompt.](/python/langchain-core/prompts/base/BasePromptTemplate)[class

PromptTemplate

Prompt template for a language model.

A prompt template consists of a string template. It accepts a set of parameters
from the user that can be used to generate a prompt for a language model.

The template can be formatted using either f-strings (default), jinja2, or mustache
syntax.

Security

Prefer using `template_format='f-string'` instead of `template_format='jinja2'`,
or make sure to NEVER accept jinja2 templates from untrusted sources as they may
lead to arbitrary Python code execution.

As of LangChain 0.0.329, Jinja2 templates will be rendered using Jinja2's
SandboxedEnvironment by default. This sand-boxing should be treated as a
best-effort approach rather than a guarantee of security, as it is an opt-out
rather than opt-in approach.

Despite the sandboxing, we recommend to never use jinja2 templates from
untrusted sources.](/python/langchain-core/prompts/prompt/PromptTemplate)[class

StructuredTool

Tool that can operate on any number of inputs.](/python/langchain-core/tools/structured/StructuredTool)[class

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

RetrieverInput

Input to the retriever.](/python/langchain-core/tools/retriever/RetrieverInput)

## Type Aliases

[typeAlias

Callbacks: list[BaseCallbackHandler] | BaseCallbackManager | None](/python/langchain-core/callbacks/base/Callbacks)


