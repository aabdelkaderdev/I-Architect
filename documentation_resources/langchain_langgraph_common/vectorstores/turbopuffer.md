<!-- Source: https://docs.langchain.com/oss/python/integrations/vectorstores/turbopuffer -->

> [turbopuffer](https://turbopuffer.com) is a fast, cost-efficient vector database for search and retrieval.

This guide shows how to use the `TurbopufferVectorStore` with LangChain.

## [​](#setup) Setup

To use the turbopuffer vector store, you need to install the `langchain-turbopuffer` integration package.

Copy

```
pip install -qU langchain-turbopuffer
```

### [​](#credentials) Credentials

Create a turbopuffer account at [turbopuffer.com](https://turbopuffer.com) and get an API key.

Copy

```
import getpass
import os

if not os.getenv("TURBOPUFFER_API_KEY"):
    os.environ["TURBOPUFFER_API_KEY"] = getpass.getpass("Enter your turbopuffer API key: ")
```

If you want to get automated tracing of your model calls you can also set your [LangSmith](https://docs.langchain.com/langsmith/home) API key by uncommenting below:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

## [​](#initialization) Initialization

Create a turbopuffer client and namespace, then initialize the vector store:

Copy

```
from langchain_openai import OpenAIEmbeddings
from turbopuffer import Turbopuffer

tpuf = Turbopuffer(region="gcp-us-central1")
ns = tpuf.namespace("langchain-test")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

Copy

```
from langchain_turbopuffer import TurbopufferVectorStore

vector_store = TurbopufferVectorStore(embedding=embeddings, namespace=ns)
```

## [​](#manage-vector-store) Manage vector store

Once you have created your vector store, you can interact with it by adding and deleting items.

### [​](#add-items-to-vector-store) Add items to vector store

Copy

```
from uuid import uuid4

from langchain_core.documents import Document

document_1 = Document(
    page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news"},
)

document_10 = Document(
    page_content="I have a bad feeling I am going to get deleted :(",
    metadata={"source": "tweet"},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)
```

### [​](#delete-items-from-vector-store) Delete items from vector store

Copy

```
vector_store.delete(ids=[uuids[-1]])
```

## [​](#query-vector-store) Query vector store

Once your vector store has been created and the relevant documents have been added you will most likely wish to query it during the running of your chain or agent.

### [​](#query-directly) Query directly

Performing a simple similarity search can be done as follows:

Copy

```
results = vector_store.similarity_search(
    "LangChain provides abstractions to make working with LLMs easy",
    k=2,
    filters=("source", "Eq", "tweet"),
)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")
```

#### [​](#similarity-search-with-score) Similarity search with score

You can also search with score. Lower distance means more similar:

Copy

```
results = vector_store.similarity_search_with_score(
    "Will it be hot tomorrow?", k=1, filters=("source", "Eq", "news")
)
for res, score in results:
    print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")
```

### [​](#query-by-turning-into-retriever) Query by turning into retriever

You can also transform the vector store into a retriever for easier usage in your chains.

Copy

```
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 1, "score_threshold": 0.4},
)
retriever.invoke("Stealing from the bank is a crime")
```

## [​](#filtering) Filtering

turbopuffer supports metadata filtering using tuple expressions. Pass filters to any search method:

Copy

```
results = vector_store.similarity_search(
    "interesting articles",
    k=2,
    filters=("source", "Eq", "website"),
)
```

See the [turbopuffer filter documentation](https://turbopuffer.com/docs/reference/query#filter-parameters) for the full list of supported filter operators.

## [​](#related) Related

- Vector store [conceptual guide](/oss/python/integrations/vectorstores)
- Vector store [how-to guides](/oss/python/integrations/vectorstores)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/vectorstores/turbopuffer.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.