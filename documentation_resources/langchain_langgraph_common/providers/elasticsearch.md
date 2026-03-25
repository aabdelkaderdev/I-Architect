<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/elasticsearch -->

> [Elasticsearch](https://www.elastic.co/elasticsearch/) is a distributed, RESTful search and analytics engine.
> It provides a distributed, multi-tenant-capable full-text search engine with an HTTP web interface and schema-free
> JSON documents.

## [​](#installation-and-setup) Installation and setup

### [​](#setup-elasticsearch) Setup Elasticsearch

There are two ways to get started with Elasticsearch:

#### [​](#install-elasticsearch-on-your-local-machine) Install Elasticsearch on your local machine

The easiest way to run Elasticsearch locally for development and testing is using the [start-local](https://github.com/elastic/start-local) script. This script sets up Elasticsearch using Docker with a simple one-line command.

Copy

```
curl -fsSL https://elastic.co/start-local | sh
```

This creates an `elastic-start-local` folder. To start Elasticsearch:

Copy

```
cd elastic-start-local
./start.sh
```

Elasticsearch will be available at `http://localhost:9200`. The password for the `elastic` user and API key are automatically generated and stored in the `.env` file in the `elastic-start-local` folder.
If you only need Elasticsearch without Kibana, you can use the `--esonly` option:

Copy

```
curl -fsSL https://elastic.co/start-local | sh -s -- --esonly
```

The start-local setup is for local testing only and should not be used in production. For production installations, refer to the official [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).

#### [​](#deploy-elasticsearch-on-elastic-cloud) Deploy Elasticsearch on elastic cloud

`Elastic Cloud` is a managed Elasticsearch service. Signup for a [free trial](https://cloud.elastic.co/registration?utm_source=langchain&utm_content=documentation).

### [​](#install-client) Install client

pip

uv

Copy

```
pip install elasticsearch
pip install langchain-elasticsearch
```

## [​](#embedding-models) Embedding models

See a [usage example](/oss/python/integrations/embeddings/elasticsearch).

Copy

```
from langchain_elasticsearch import ElasticsearchEmbeddings
```

## [​](#vector-store) Vector store

See a [usage example](/oss/python/integrations/vectorstores/elasticsearch).

Copy

```
from langchain_elasticsearch import ElasticsearchStore
```

### [​](#third-party-integrations) Third-party integrations

#### [​](#ecloudesvectorstore) EcloudESVectorStore

Copy

```
from langchain_community.vectorstores.ecloud_vector_search import EcloudESVectorStore
```

## [​](#retrievers) Retrievers

### [​](#elasticsearchretriever) ElasticsearchRetriever

The `ElasticsearchRetriever` enables flexible access to all Elasticsearch features
through the Query DSL.
See a [usage example](/oss/python/integrations/retrievers/elasticsearch_retriever).

Copy

```
from langchain_elasticsearch import ElasticsearchRetriever
```

### [​](#bm25) BM25

See a [usage example](/oss/python/integrations/retrievers/elastic_search_bm25).

Copy

```
from langchain_community.retrievers import ElasticSearchBM25Retriever
```

## [​](#llm-cache) LLM cache

Copy

```
from langchain_elasticsearch import ElasticsearchCache
```

## [​](#byte-store) Byte store

See a [usage example](/oss/python/integrations/stores/elasticsearch).

Copy

```
from langchain_elasticsearch import ElasticsearchEmbeddingsCache
```

## [​](#chain) Chain

It is a chain for interacting with Elasticsearch Database.

Copy

```
from langchain_classic.chains.elasticsearch_database import ElasticsearchDatabaseChain
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/elasticsearch.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.