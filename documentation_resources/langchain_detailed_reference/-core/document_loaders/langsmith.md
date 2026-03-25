<!-- Source: https://reference.langchain.com/python/langchain-core/document_loaders/langsmith -->

Modulev1.2.21 (latest)●Since v0.2

# langsmith

LangSmith document loader.

## Functions

[function

pydantic\_to\_dict

Convert any Pydantic model to dict, compatible with both v1 and v2.](/python/langchain-core/tracers/_compat/pydantic_to_dict)

## Classes

[class

BaseLoader

Interface for document loader.

Implementations should implement the lazy-loading method using generators to avoid
loading all documents into memory at once.

`load` is provided just for user convenience and should not be overridden.](/python/langchain-core/document_loaders/base/BaseLoader)[class

Document

Class for storing a piece of text and associated metadata.

Note

`Document` is for **retrieval workflows**, not chat I/O. For sending text
to an LLM in a conversation, use message types from `langchain.messages`.](/python/langchain-core/documents/base/Document)[class

LangSmithLoader

Load LangSmith Dataset examples as `Document` objects.

Loads the example inputs as the `Document` page content and places the entire
example into the `Document` metadata. This allows you to easily create few-shot
example retrievers from the loaded documents.

Lazy loading

```
from langchain_core.document_loaders import LangSmithLoader

loader = LangSmithLoader(dataset_id="...", limit=100)
docs = []
for doc in loader.lazy_load():
    docs.append(doc)
```

```
# -> [Document("...", metadata={"inputs": {...}, "outputs": {...}, ...}), ...]
```](/python/langchain-core/document_loaders/langsmith/LangSmithLoader)


