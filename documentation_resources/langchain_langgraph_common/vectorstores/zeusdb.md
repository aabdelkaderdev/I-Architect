<!-- Source: https://docs.langchain.com/oss/python/integrations/vectorstores/zeusdb -->

> [ZeusDB](https://www.zeusdb.com) is a high-performance vector database powered by Rust, offering advanced features like product quantization, persistent storage, and enterprise-grade logging.

This documentation shows how to use ZeusDB to bring enterprise-grade vector search capabilities to your LangChain applications.

---

## [​](#setup) Setup

Install the ZeusDB LangChain integration package from PyPi:

Copy

```
pip install -qU langchain-zeusdb
```

Setup in Jupyter Notebooks

Copy

```
pip install -qU langchain-zeusdb
```

---

## [​](#getting-started) Getting started

This example uses OpenAIEmbeddings, which requires an OpenAI API key: [Get your OpenAI API key here](https://platform.openai.com/api-keys)
If you prefer, you can also use this package with any other embedding provider (Hugging Face, Cohere, custom functions, etc.).
Install the LangChain OpenAI integration package from PyPi:

Copy

```
pip install -qU langchain-openai

# Use this command if inside Jupyter Notebooks
#pip install -qU langchain-openai
```

#### [​](#please-choose-an-option-below-for-your-openai-key-integration) Please choose an option below for your OpenAI key integration

*Option 1: 🔑 Enter your API key each time*
Use getpass in Jupyter to securely input your key for the current session:

Copy

```
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

*Option 2: 🗂️ Use a .env file*
Keep your key in a local .env file and load it automatically with python-dotenv

Copy

```
from dotenv import load_dotenv

load_dotenv()  # reads .env and sets OPENAI_API_KEY
```

🎉 Nicely done! You are good to go.

---

## [​](#initialization) Initialization

Copy

```
# Import required Packages and Classes
from langchain_zeusdb import ZeusDBVectorStore
from langchain_openai import OpenAIEmbeddings
from zeusdb import VectorDatabase
```

Copy

```
# Initialize embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create ZeusDB index
vdb = VectorDatabase()
index = vdb.create(index_type="hnsw", dim=1536, space="cosine")

# Create vector store
vector_store = ZeusDBVectorStore(zeusdb_index=index, embedding=embeddings)
```

---

## [​](#manage-vector-store) Manage vector store

### [​](#2-1-add-items-to-vector-store) 2.1 add items to vector store

Copy

```
from langchain_core.documents import Document

document_1 = Document(
    page_content="ZeusDB is a high-performance vector database",
    metadata={"source": "https://docs.zeusdb.com"},
)

document_2 = Document(
    page_content="Product Quantization reduces memory usage significantly",
    metadata={"source": "https://docs.zeusdb.com"},
)

document_3 = Document(
    page_content="ZeusDB integrates seamlessly with LangChain",
    metadata={"source": "https://docs.zeusdb.com"},
)

documents = [document_1, document_2, document_3]

vector_store.add_documents(documents=documents, ids=["1", "2", "3"])
```

### [​](#2-2-update-items-in-vector-store) 2.2 update items in vector store

Copy

```
updated_document = Document(
    page_content="ZeusDB now supports advanced Product Quantization with 4x-256x compression",
    metadata={"source": "https://docs.zeusdb.com", "updated": True},
)

vector_store.add_documents([updated_document], ids=["1"])
```

### [​](#2-3-delete-items-from-vector-store) 2.3 delete items from vector store

Copy

```
vector_store.delete(ids=["3"])
```

---

## [​](#query-vector-store) Query vector store

### [​](#3-1-query-directly) 3.1 query directly

Performing a simple similarity search:

Copy

```
results = vector_store.similarity_search(query="high performance database", k=2)

for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

If you want to execute a similarity search and receive the corresponding scores:

Copy

```
results = vector_store.similarity_search_with_score(query="memory optimization", k=2)

for doc, score in results:
    print(f"* [SIM={score:.3f}] {doc.page_content} [{doc.metadata}]")
```

### [​](#3-2-query-by-turning-into-retriever) 3.2 query by turning into retriever

You can also transform the vector store into a retriever for easier usage in your chains:

Copy

```
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})

retriever.invoke("vector database features")
```

---

## [​](#zeusdb-specific-features) ZeusDB-Specific features

### [​](#4-1-memory-efficient-setup-with-product-quantization) 4.1 Memory-Efficient setup with product quantization

For large datasets, use Product Quantization to reduce memory usage:

Copy

```
# Create memory-optimized vector store
quantization_config = {"type": "pq", "subvectors": 8, "bits": 8, "training_size": 10000}

vdb_quantized = VectorDatabase()
quantized_index = vdb_quantized.create(
    index_type="hnsw", dim=1536, quantization_config=quantization_config
)

quantized_vector_store = ZeusDBVectorStore(
    zeusdb_index=quantized_index, embedding=embeddings
)

print(f"Created quantized store: {quantized_index.info()}")
```

### [​](#4-2-persistence) 4.2 persistence

Save and load your vector store to disk:
How to Save your vector store

Copy

```
# Save the vector store
vector_store.save_index("my_zeusdb_index.zdb")
```

How to Load your vector store

Copy

```
# Load the vector store
loaded_store = ZeusDBVectorStore.load_index(
    path="my_zeusdb_index.zdb", embedding=embeddings
)

print(f"Loaded store with {loaded_store.get_vector_count()} vectors")
```

---

## [​](#usage-for-retrieval-augmented-generation) Usage for retrieval-augmented generation

For guides on how to use this vector store for retrieval-augmented generation (RAG), see the following sections:

- [How-to: Question and answer with RAG](https://python.langchain.com/docs/how_to/#qa-with-rag)
- [Retrieval conceptual docs](https://python.langchain.com/docs/concepts/retrieval/)

---

## [​](#api-reference) API reference

For detailed documentation of all ZeusDBVectorStore features and configurations head to [ZeusDB Docs](https://docs.zeusdb.com/en/latest/vector_database/integrations/langchain.html).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/vectorstores/zeusdb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.