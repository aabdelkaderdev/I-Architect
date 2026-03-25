<!-- Source: https://docs.langchain.com/oss/python/integrations/vectorstores/cockroachdb -->

`AsyncCockroachDBVectorStore` is an implementation of a LangChain vector store using CockroachDB’s distributed SQL database with native vector support.
This notebook goes over how to use the `AsyncCockroachDBVectorStore` API.
The code lives in the integration package: [langchain-cockroachdb](https://github.com/cockroachdb/langchain-cockroachdb/).

## [​](#overview) Overview

CockroachDB is a distributed SQL database that provides:

- **Native vector support** with the `VECTOR` data type (v24.2+)
- **Distributed C-SPANN indexes** for approximate nearest neighbor (ANN) search (v25.2+)
- **SERIALIZABLE isolation** by default for transaction correctness
- **Horizontal scalability** with automatic sharding and replication
- **PostgreSQL wire-compatible** for easy adoption

### [​](#key-advantages-for-vector-workloads) Key advantages for vector workloads

- **Distributed vector indexes**: C-SPANN indexes automatically shard across your cluster
- **Multi-tenancy support**: Prefix columns in indexes for efficient tenant isolation
- **Strong consistency**: SERIALIZABLE transactions prevent data anomalies
- **High availability**: Automatic failover with no data loss

## [​](#setup) Setup

### [​](#install) Install

Install the integration library, `langchain-cockroachdb`.

Copy

```
pip install -qU langchain-cockroachdb
```

### [​](#cockroachdb-cluster) CockroachDB cluster

You need a CockroachDB cluster with vector support (v24.2+). Choose one option:

#### [​](#option-1-cockroachdb-cloud-recommended) Option 1: CockroachDB Cloud (Recommended)

1. Sign up at [cockroachlabs.cloud](https://cockroachlabs.cloud)
2. Create a free cluster
3. Get your connection string from the cluster details page

#### [​](#option-2-docker-development) Option 2: Docker (Development)

Copy

```
docker run -d \
  --name cockroachdb \
  -p 26257:26257 \
  -p 8080:8080 \
  cockroachdb/cockroach:latest \
  start-single-node --insecure
```

#### [​](#option-3-local-binary) Option 3: Local binary

Download from [cockroachlabs.com/docs/releases](https://www.cockroachlabs.com/docs/releases/)

Copy

```
cockroach start-single-node --insecure --listen-addr=localhost:26257
```

### [​](#set-your-connection-values) Set your connection values

Copy

```
# For CockroachDB Cloud
CONNECTION_STRING = "cockroachdb://user:password@host:26257/database?sslmode=verify-full"

# For local insecure cluster
CONNECTION_STRING = "cockroachdb://root@localhost:26257/defaultdb?sslmode=disable"

TABLE_NAME = "langchain_vectors"
VECTOR_DIMENSION = 1536  # Depends on your embedding model
```

## [​](#initialization) Initialization

### [​](#create-a-connection-engine) Create a connection engine

The `CockroachDBEngine` manages a connection pool to your cluster:

Copy

```
from langchain_cockroachdb import CockroachDBEngine

engine = CockroachDBEngine.from_connection_string(
    url=CONNECTION_STRING,
    pool_size=10,        # Connection pool size
    max_overflow=20,     # Additional connections allowed
    pool_pre_ping=True,  # Health check connections
)
```

### [​](#initialize-a-table) Initialize a table

Create a table with the proper schema for vector storage:

Copy

```
await engine.ainit_vectorstore_table(
    table_name=TABLE_NAME,
    vector_dimension=VECTOR_DIMENSION,
)
```

**Optional**: Specify a schema name

Copy

```
await engine.ainit_vectorstore_table(
    table_name=TABLE_NAME,
    vector_dimension=VECTOR_DIMENSION,
    schema="my_schema",  # Default: "public"
)
```

### [​](#create-an-embedding-instance) Create an embedding instance

Use any [LangChain embeddings model](https://python.langchain.com/docs/integrations/embeddings/).

Copy

```
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

### [​](#initialize-the-vector-store) Initialize the vector store

Copy

```
from langchain_cockroachdb import AsyncCockroachDBVectorStore

vectorstore = AsyncCockroachDBVectorStore(
    engine=engine,
    embeddings=embeddings,
    collection_name=TABLE_NAME,
)
```

## [​](#manage-vector-store) Manage vector store

### [​](#add-documents) Add documents

Add documents with metadata:

Copy

```
import uuid
from langchain_core.documents import Document

docs = [
    Document(
        id=str(uuid.uuid4()),
        page_content="CockroachDB is a distributed SQL database",
        metadata={"source": "docs", "category": "database"},
    ),
    Document(
        id=str(uuid.uuid4()),
        page_content="Vector search enables semantic similarity",
        metadata={"source": "docs", "category": "features"},
    ),
]

ids = await vectorstore.aadd_documents(docs)
```

### [​](#add-texts) Add texts

Add text directly without structuring as documents:

Copy

```
texts = ["First text", "Second text", "Third text"]
metadatas = [{"idx": i} for i in range(len(texts))]
ids = [str(uuid.uuid4()) for _ in texts]

ids = await vectorstore.aadd_texts(texts, metadatas=metadatas, ids=ids)
```

**Performance note**: CockroachDB’s vector indexes work best with smaller batch sizes. The default `batch_size=100` is optimized for vector inserts. Large batch inserts of VECTOR types can cause performance degradation.

### [​](#delete-documents) Delete documents

Delete documents by ID:

Copy

```
await vectorstore.adelete([ids[0], ids[1]])
```

## [​](#query-vector-store) Query vector store

### [​](#similarity-search) Similarity search

Search for similar documents using natural language:

Copy

```
query = "distributed database"
docs = await vectorstore.asimilarity_search(query, k=5)

for doc in docs:
    print(f"{doc.page_content[:50]}...")
```

### [​](#similarity-search-with-scores) Similarity search with scores

Get relevance scores with results:

Copy

```
docs_with_scores = await vectorstore.asimilarity_search_with_score(query, k=5)

for doc, score in docs_with_scores:
    print(f"Score: {score:.4f} - {doc.page_content[:50]}...")
```

### [​](#search-by-vector) Search by vector

Search using a pre-computed embedding vector:

Copy

```
query_vector = await embeddings.aembed_query(query)
docs = await vectorstore.asimilarity_search_by_vector(query_vector, k=5)
```

### [​](#maximum-marginal-relevance-mmr-search) Maximum marginal relevance (MMR) search

Retrieve diverse results that balance relevance and diversity:

Copy

```
docs = await vectorstore.amax_marginal_relevance_search(
    query,
    k=5,           # Number of results to return
    fetch_k=20,    # Number of candidates to consider
    lambda_mult=0.5,  # 0 = max diversity, 1 = max relevance
)
```

## [​](#vector-indexes) Vector indexes

Speed up similarity search with CockroachDB’s C-SPANN vector indexes (requires v25.2+).

### [​](#what-is-c-spann) What is C-SPANN?

C-SPANN (CockroachDB Space Partition Approximate Nearest Neighbor) is a distributed vector index that:

- Automatically shards across your cluster nodes
- Provides sub-second query performance at scale
- Supports cosine, Euclidean (L2), and inner product distances
- Works with prefix columns for multi-tenant architectures

### [​](#create-a-vector-index) Create a vector index

Copy

```
from langchain_cockroachdb import CSPANNIndex, DistanceStrategy

# Create a cosine distance index (most common)
index = CSPANNIndex(
    distance_strategy=DistanceStrategy.COSINE,
    name="my_vector_index",
)

await vectorstore.aapply_vector_index(index)
```

### [​](#distance-strategies) Distance strategies

Choose the distance metric that matches your use case:

Copy

```
# Cosine similarity (most common for text embeddings)
CSPANNIndex(distance_strategy=DistanceStrategy.COSINE)

# Euclidean distance (L2)
CSPANNIndex(distance_strategy=DistanceStrategy.EUCLIDEAN)

# Inner product (for normalized vectors)
CSPANNIndex(distance_strategy=DistanceStrategy.INNER_PRODUCT)
```

### [​](#tune-index-parameters) Tune index parameters

Adjust partition sizes for performance:

Copy

```
index = CSPANNIndex(
    distance_strategy=DistanceStrategy.COSINE,
    min_partition_size=16,   # Minimum vectors per partition
    max_partition_size=128,  # Maximum vectors per partition
)

await vectorstore.aapply_vector_index(index)
```

### [​](#query-time-tuning) Query-time tuning

Adjust search parameters at query time:

Copy

```
from langchain_cockroachdb import CSPANNQueryOptions

# Increase beam size for better recall (slower)
query_options = CSPANNQueryOptions(beam_size=200)  # Default: 100

docs = await vectorstore.asimilarity_search(
    query,
    k=10,
    query_options=query_options,
)
```

### [​](#drop-an-index) Drop an index

Remove a vector index:

Copy

```
index = CSPANNIndex(name="my_vector_index")
await vectorstore.adrop_vector_index(index)
```

## [​](#metadata-filtering) Metadata filtering

Filter similarity searches using metadata fields.

### [​](#supported-operators) Supported operators

| Operator | Meaning | Example |
| --- | --- | --- |
| `$eq` | Equality | `{"category": "news"}` |
| `$ne` | Not equal | `{"category": {"$ne": "spam"}}` |
| `$gt` | Greater than | `{"year": {"$gt": 2020}}` |
| `$gte` | Greater than or equal | `{"rating": {"$gte": 4.0}}` |
| `$lt` | Less than | `{"year": {"$lt": 2023}}` |
| `$lte` | Less than or equal | `{"rating": {"$lte": 3.0}}` |
| `$in` | In list | `{"category": {"$in": ["news", "blog"]}}` |
| `$nin` | Not in list | `{"source": {"$nin": ["spam", "test"]}}` |
| `$between` | Between values | `{"year": {"$between": [2020, 2023]}}` |
| `$like` | Pattern match | `{"source": {"$like": "wiki%"}}` |
| `$ilike` | Case-insensitive | `{"category": {"$ilike": "%NEWS%"}}` |
| `$and` | Logical AND | `{"$and": [{...}, {...}]}` |
| `$or` | Logical OR | `{"$or": [{...}, {...}]}` |

### [​](#filter-examples) Filter examples

Copy

```
# Simple equality
docs = await vectorstore.asimilarity_search(
    query,
    filter={"category": "news"},
)

# Numeric comparison
docs = await vectorstore.asimilarity_search(
    query,
    filter={"year": {"$gte": 2020}},
)

# Complex filters
docs = await vectorstore.asimilarity_search(
    query,
    filter={
        "$and": [
            {"category": {"$in": ["news", "blog"]}},
            {"year": {"$gte": 2020}},
            {"rating": {"$gt": 3.5}},
        ]
    },
)
```

## [​](#sync-interface) Sync interface

All async methods have sync equivalents using the sync wrapper:

Copy

```
from langchain_cockroachdb import CockroachDBVectorStore

# Create sync vectorstore
vectorstore = CockroachDBVectorStore(
    engine=engine,
    embeddings=embeddings,
    collection_name=TABLE_NAME,
)

# Use sync methods
docs = vectorstore.similarity_search(query, k=5)
ids = vectorstore.add_documents(docs)
vectorstore.apply_vector_index(index)
```

## [​](#usage-for-retrieval-augmented-generation-rag) Usage for retrieval-augmented generation (RAG)

For implementing RAG with CockroachDB as your vector store, see the [LangChain RAG tutorial](/oss/python/langchain/rag). The CockroachDB vector store can be used in place of any other vector store in those patterns.

## [​](#clean-up) Clean up

**⚠️ This operation cannot be undone**

Drop the vector store table:

Copy

```
await engine.adrop_table(TABLE_NAME)
```

## [​](#api-reference) API reference

For detailed documentation of all features and configurations:

- [GitHub repository](https://github.com/cockroachdb/langchain-cockroachdb)
- [PyPI package](https://pypi.org/project/langchain-cockroachdb/)

## [​](#additional-resources) Additional resources

- [CockroachDB Vector Indexes documentation](https://www.cockroachlabs.com/docs/stable/vector-indexes)
- [CockroachDB Cloud](https://cockroachlabs.cloud)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/vectorstores/cockroachdb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.