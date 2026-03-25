<!-- Source: https://docs.langchain.com/oss/python/integrations/vectorstores/lambdadb -->

> [LambdaDB](https://lambdadb.ai/) is a serverless AI database for building scalable RAG and agent applications.

This notebook covers how to get started with the LambdaDB vector store in LangChain.

## [​](#setup) Setup

To access the LambdaDB vector store, you’ll need to create a LambdaDB account, get your project credentials, and install the `langchain-lambdadb` integration package.

### [​](#credentials) Credentials

LambdaDB uses project-based authentication with a project URL and API key:

Copy

```
import getpass
import os

if "LAMBDADB_PROJECT_URL" not in os.environ:
    os.environ["LAMBDADB_PROJECT_URL"] = getpass.getpass("Enter your LambdaDB project URL: ")

if "LAMBDADB_API_KEY" not in os.environ:
    os.environ["LAMBDADB_API_KEY"] = getpass.getpass("Enter your LambdaDB API key: ")
```

To enable automated tracing of your model calls, set your [LangSmith](/langsmith/home) API key:

Copy

```
os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API key: ")
os.environ["LANGSMITH_TRACING"] = "true"
```

### [​](#installation) Installation

The LangChain LambdaDB integration lives in the `langchain-lambdadb` package:

Copy

```
pip install -U langchain-lambdadb
```

You’ll also need to install an embedding model. For example, to use OpenAI embeddings:

Copy

```
pip install -U langchain-openai
```

---

## [​](#instantiation) Instantiation

`LambdaDBVectorStore` works with existing collections. You must create the collection beforehand with proper vector and text indexes configured.

Copy

```
from langchain_lambdadb.vectorstores import LambdaDBVectorStore
from langchain_openai import OpenAIEmbeddings
from lambdadb import LambdaDB
import os

# Initialize the LambdaDB client
client = LambdaDB(
    server_url=os.environ["LAMBDADB_SERVER_URL"],
    project_api_key=os.environ["LAMBDADB_API_KEY"]
)

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Connect to an existing collection
vector_store = LambdaDBVectorStore(
    client=client,
    collection_name="my_collection",  # Must exist beforehand
    embedding=embeddings,
)
```

### [​](#key-parameters) Key parameters

- `client`: LambdaDB client instance (required)
- `collection_name`: Name of an existing collection in LambdaDB (required)
- `embedding`: Embedding function to use (required)
- `text_field`: Name of the text field in documents (default: “text”)
- `vector_field`: Name of the vector field in documents (default: “vector”)
- `validate_collection`: Whether to validate that the collection exists and is active (default: True)
- `default_consistent_read`: Use consistent reads by default for immediate consistency, or eventual consistency for better performance (default: False)

---

## [​](#manage-vector-store) Manage vector store

### [​](#add-items) Add items

Copy

```
from langchain_core.documents import Document

document_1 = Document(page_content="LambdaDB is a serverless vector database", metadata={"source": "docs"})
document_2 = Document(page_content="It supports fast similarity search", metadata={"source": "docs"})
document_3 = Document(page_content="Perfect for RAG applications", metadata={"category": "features"})

documents = [document_1, document_2, document_3]
ids = vector_store.add_documents(documents=documents, ids=["1", "2", "3"])
print(f"Added documents with IDs: {ids}")
```

Documents have a maximum size of 50KB. The integration automatically batches documents into groups of up to 100 to stay within LambdaDB’s 6MB request limit.

### [​](#delete-items) Delete items

Copy

```
vector_store.delete(ids=["3"])
```

### [​](#get-items-by-id) Get items by ID

Copy

```
documents = vector_store.get_by_ids(["1", "2"])
for doc in documents:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

---

## [​](#query-vector-store) Query vector store

Once your vector store has been created and the relevant documents have been added, you will most likely wish to query it during the running of your chain or agent.

### [​](#similarity-search) Similarity search

Performing a simple similarity search:

Copy

```
results = vector_store.similarity_search(
    query="What is LambdaDB?",
    k=2
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

### [​](#similarity-search-with-scores) Similarity search with scores

If you want to execute a similarity search and receive the corresponding scores:

Copy

```
results = vector_store.similarity_search_with_score(
    query="vector database features",
    k=2
)
for doc, score in results:
    print(f"* [SIM={score:.3f}] {doc.page_content} [{doc.metadata}]")
```

### [​](#similarity-search-with-filtering) Similarity search with filtering

LambdaDB supports filtering using query string syntax:

Copy

```
results = vector_store.similarity_search(
    query="database",
    k=2,
    filter={"queryString": {"query": "source:docs"}}
)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

### [​](#maximal-marginal-relevance-mmr-search) Maximal Marginal Relevance (MMR) search

MMR optimizes for both similarity to the query AND diversity among selected documents:

Copy

```
results = vector_store.max_marginal_relevance_search(
    query="LambdaDB features",
    k=2,
    fetch_k=10,  # Fetch 10 candidates
    lambda_mult=0.5,  # Balance between relevance (1.0) and diversity (0.0)
)
for doc in results:
    print(f"* {doc.page_content}")
```

### [​](#turn-into-retriever) Turn into retriever

You can also transform the vector store into a retriever for easier usage in your chains:

Copy

```
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2, "fetch_k": 10}
)
retriever.invoke("What is LambdaDB?")
```

Supported search types:

- `"similarity"`: Standard similarity search (default)
- `"mmr"`: Maximal marginal relevance search
- `"similarity_score_threshold"`: Similarity search with a score threshold

---

## [​](#async-operations) Async operations

`LambdaDBVectorStore` supports async methods for all operations:

Copy

```
# Add documents
ids = await vector_store.aadd_documents(documents=documents)

# Delete documents
await vector_store.adelete(ids=["3"])

# Search
results = await vector_store.asimilarity_search(query="LambdaDB", k=2)
for doc in results:
    print(f"* {doc.page_content}")

# Search with score
results = await vector_store.asimilarity_search_with_score(query="database", k=2)
for doc, score in results:
    print(f"* [SIM={score:.3f}] {doc.page_content}")
```

Currently, async methods run synchronously as the LambdaDB client doesn’t support async operations yet.

---

## [​](#consistency-control) Consistency control

LambdaDB supports two consistency modes:

- **Eventual consistency** (default): Faster performance, but data may be up to ~1 minute stale after writes
- **Consistent reads**: Immediate consistency, slight performance impact

Copy

```
# Use consistent reads for a specific operation
results = vector_store.similarity_search(
    query="LambdaDB",
    k=2,
    consistent_read=True
)

# Or set consistent reads as the default
vector_store = LambdaDBVectorStore(
    client=client,
    collection_name="my_collection",
    embedding=embeddings,
    default_consistent_read=True  # All reads will be consistent by default
)
```

---

## [​](#creating-from-texts) Creating from texts

You can create a vector store and populate it with texts in one step:

Copy

```
from langchain_lambdadb.vectorstores import LambdaDBVectorStore

texts = [
    "LambdaDB is a serverless vector database",
    "It supports fast similarity search",
    "Perfect for RAG applications"
]

metadatas = [
    {"source": "docs"},
    {"source": "docs"},
    {"category": "features"}
]

vector_store = LambdaDBVectorStore.from_texts(
    texts=texts,
    embedding=embeddings,
    metadatas=metadatas,
    client=client,
    collection_name="my_collection",
    ids=["1", "2", "3"]
)
```

---

## [​](#usage-for-retrieval-augmented-generation) Usage for retrieval-augmented generation

Here’s a complete example using LambdaDB for RAG:

Copy

```
from langchain_lambdadb.vectorstores import LambdaDBVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from lambdadb import LambdaDB
import os

# Initialize
client = LambdaDB(
    project_url=os.environ["LAMBDADB_PROJECT_URL"],
    project_api_key=os.environ["LAMBDADB_API_KEY"]
)

embeddings = OpenAIEmbeddings()
vector_store = LambdaDBVectorStore(
    client=client,
    collection_name="my_collection",
    embedding=embeddings
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Create RAG chain
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Use the chain
response = chain.invoke("What is LambdaDB?")
print(response)
```

---

## [​](#key-features) Key features

### [​](#document-size-limits) Document size limits

- Maximum document size: 50KB per document
- The integration validates document sizes and raises an error if exceeded

### [​](#batch-processing) Batch processing

- Documents are automatically batched in groups of 100 for upsert operations
- Stays within LambdaDB’s 6MB request limit

### [​](#filtering) Filtering

- Supports LambdaDB’s query string syntax for metadata filtering
- Example: `filter={"queryString": {"query": "field:value"}}`

### [​](#search-options) Search options

- **Similarity search**: Find documents similar to a query
- **MMR search**: Balance similarity and diversity
- **Score thresholding**: Filter results by similarity score
- **Consistent reads**: Control read consistency vs. performance trade-off

---

## [​](#api-reference) API reference

For detailed documentation of all `LambdaDBVectorStore` features and configurations, head to the [API reference](https://docs.lambdadb.ai/guides/get-started/quickstart).

---

## [​](#additional-resources) Additional resources

- [LambdaDB Documentation](https://docs.lambdadb.ai)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/vectorstores/lambdadb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.