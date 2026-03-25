<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/azure_ai -->

This page covers all LangChain integrations with [Microsoft Azure](https://azure.microsoft.com/) and its related projects.
Integration packages for Azure AI, Dynamic Sessions, SQL Server are maintained in
the [langchain-azure](https://github.com/langchain-ai/langchain-azure) repository.

## [​](#chat-models) Chat models

We recommend developers start with the (`langchain-azure-ai`) to access all the models available in [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/model-catalog-overview).

### [​](#azure-ai-chat-completions) Azure AI chat completions

Access models like Azure OpenAI, DeepSeek R1, Cohere, Phi and Mistral using the `AzureAIOpenAIApiChatModel` class.

pip

uv

Copy

```
pip install -U langchain-azure-ai
```

Configure your endpoint. You can use a project endpoint with `DefaultAzureCredential`, or set an API key directly.

Copy

```
export AZURE_AI_PROJECT_ENDPOINT=your-project-endpoint
```

Copy

```
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel
from azure.identity import DefaultAzureCredential

llm = AzureAIOpenAIApiChatModel(
    model="gpt-4.1",
    credential=DefaultAzureCredential(),
)

llm.invoke('Tell me a joke and include some emojis')
```

## [​](#embedding-models) Embedding models

### [​](#azure-ai-model-inference-for-embeddings) Azure AI model inference for embeddings

pip

uv

Copy

```
pip install -U langchain-azure-ai
```

Configure your endpoint. You can use a project endpoint with `DefaultAzureCredential`, or set an API key directly.

Copy

```
export AZURE_AI_PROJECT_ENDPOINT=your-project-endpoint
```

Copy

```
from langchain_azure_ai.embeddings import AzureAIOpenAIApiEmbeddingsModel
from azure.identity import DefaultAzureCredential

embed_model = AzureAIOpenAIApiEmbeddingsModel(
    model="text-embedding-ada-002",
    credential=DefaultAzureCredential(),
)
```

## [​](#vector-stores) Vector stores

### [​](#azure-cosmosdb-nosql-vector-search) Azure CosmosDB NoSQL vector search

> [Azure CosmosDB NoSQL](https://azure.microsoft.com/en-us/products/cosmos-db/) is a fully managed,
> globally distributed, serverless document database for modern applications. It stores data in flexible
> JSON documents and uses a SQL-like query language. This provides high performance, low latency, and automatic,
> elastic scalability. It also features integrated vector search capabilities for AI workloads
> like generative AI and RAG. This allows you to store, index, and query vector embeddings alongside
> your operational data in the same database. You can combine vector similarity search with traditional
> keyword-based search for relevant results and choose from various indexing methods for optimal performance.
> This unified approach simplifies application architecture and ensures data consistency.

We need to install the `azure-cosmos` package to use this vector store.

pip

uv

Copy

```
pip install -qU azure-cosmos
```

Copy

```
from langchain_azure_ai.vectorstores.azure_cosmos_db_no_sql import (
    AzureCosmosDBNoSqlVectorSearch,
)
vector_search = AzureCosmosDBNoSqlVectorSearch.from_documents(
    documents=docs,
    embedding=openai_embeddings,
    cosmos_client=cosmos_client,
    database_name=database_name,
    container_name=container_name,
    vector_embedding_policy=vector_embedding_policy,
    full_text_policy=full_text_policy,
    indexing_policy=indexing_policy,
    cosmos_container_properties=cosmos_container_properties,
    cosmos_database_properties={},
    full_text_search_enabled=True,
)
```

See a [usage example](/oss/python/integrations/vectorstores/azure_cosmos_db_no_sql).

### [​](#azure-cosmosdb-mongo-vcore-vector-search) Azure CosmosDB mongo vCore vector search

> [Azure CosmosDB Mongo vCore](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/) architecture makes
> it easy to create a database with full native MongoDB support. You can apply your MongoDB experience and continue
> to use your favorite MongoDB drivers, SDKs, and tools by pointing your application to the API for MongoDB (vCore)
> cluster’s connection string.

We need to install the `pymongo` package to use this vector store.

pip

uv

Copy

```
pip install -qU pymongo
```

Copy

```
from langchain_azure_ai.vectorstores.azure_cosmos_db_mongo_vcore import (
    AzureCosmosDBMongoVCoreVectorSearch,
)

vectorstore = AzureCosmosDBMongoVCoreVectorSearch.from_documents(
    docs,
    openai_embeddings,
    collection=collection,
    index_name=INDEX_NAME,
)
```

See a [usage example](/oss/python/integrations/vectorstores/azure_cosmos_db_mongo_vcore).

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/azure_ai.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.