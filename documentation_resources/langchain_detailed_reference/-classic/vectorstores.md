<!-- Source: https://reference.langchain.com/python/langchain-classic/vectorstores -->

Modulev1.2.13 (latest)●Since v1.0

# vectorstores

**Vector store** stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/vectorstores/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Modules

[module

xata](/python/langchain-classic/vectorstores/xata)[module

semadb](/python/langchain-classic/vectorstores/semadb)[module

momento\_vector\_index](/python/langchain-classic/vectorstores/momento_vector_index)[module

cassandra](/python/langchain-classic/vectorstores/cassandra)[module

clickhouse](/python/langchain-classic/vectorstores/clickhouse)[module

zep](/python/langchain-classic/vectorstores/zep)[module

hippo](/python/langchain-classic/vectorstores/hippo)[module

vearch](/python/langchain-classic/vectorstores/vearch)[module

vectara](/python/langchain-classic/vectorstores/vectara)[module

rocksetdb](/python/langchain-classic/vectorstores/rocksetdb)[module

azuresearch](/python/langchain-classic/vectorstores/azuresearch)[module

analyticdb](/python/langchain-classic/vectorstores/analyticdb)[module

pinecone](/python/langchain-classic/vectorstores/pinecone)[module

base](/python/langchain-classic/vectorstores/base)[module

singlestoredb](/python/langchain-classic/vectorstores/singlestoredb)[module

vespa](/python/langchain-classic/vectorstores/vespa)[module

tair](/python/langchain-classic/vectorstores/tair)[module

meilisearch](/python/langchain-classic/vectorstores/meilisearch)[module

scann](/python/langchain-classic/vectorstores/scann)[module

lancedb](/python/langchain-classic/vectorstores/lancedb)[module

mongodb\_atlas](/python/langchain-classic/vectorstores/mongodb_atlas)[module

clarifai](/python/langchain-classic/vectorstores/clarifai)[module

baiducloud\_vector\_search](/python/langchain-classic/vectorstores/baiducloud_vector_search)[module

weaviate](/python/langchain-classic/vectorstores/weaviate)[module

atlas](/python/langchain-classic/vectorstores/atlas)[module

neo4j\_vector](/python/langchain-classic/vectorstores/neo4j_vector)[module

starrocks](/python/langchain-classic/vectorstores/starrocks)[module

databricks\_vector\_search](/python/langchain-classic/vectorstores/databricks_vector_search)[module

utils](/python/langchain-classic/vectorstores/utils)[module

chroma](/python/langchain-classic/vectorstores/chroma)[module

opensearch\_vector\_search](/python/langchain-classic/vectorstores/opensearch_vector_search)[module

dashvector](/python/langchain-classic/vectorstores/dashvector)[module

milvus](/python/langchain-classic/vectorstores/milvus)[module

tencentvectordb](/python/langchain-classic/vectorstores/tencentvectordb)[module

pgembedding](/python/langchain-classic/vectorstores/pgembedding)[module

pgvector](/python/langchain-classic/vectorstores/pgvector)[module

sqlitevss](/python/langchain-classic/vectorstores/sqlitevss)[module

hologres](/python/langchain-classic/vectorstores/hologres)[module

pgvecto\_rs](/python/langchain-classic/vectorstores/pgvecto_rs)[module

usearch](/python/langchain-classic/vectorstores/usearch)[module

timescalevector](/python/langchain-classic/vectorstores/timescalevector)[module

qdrant](/python/langchain-classic/vectorstores/qdrant)[module

llm\_rails](/python/langchain-classic/vectorstores/llm_rails)[module

tiledb](/python/langchain-classic/vectorstores/tiledb)[module

marqo](/python/langchain-classic/vectorstores/marqo)[module

elasticsearch](/python/langchain-classic/vectorstores/elasticsearch)[module

epsilla](/python/langchain-classic/vectorstores/epsilla)[module

supabase](/python/langchain-classic/vectorstores/supabase)[module

typesense](/python/langchain-classic/vectorstores/typesense)[module

myscale](/python/langchain-classic/vectorstores/myscale)[module

zilliz](/python/langchain-classic/vectorstores/zilliz)[module

dingo](/python/langchain-classic/vectorstores/dingo)[module

annoy](/python/langchain-classic/vectorstores/annoy)[module

matching\_engine](/python/langchain-classic/vectorstores/matching_engine)[module

faiss](/python/langchain-classic/vectorstores/faiss)[module

nucliadb](/python/langchain-classic/vectorstores/nucliadb)[module

deeplake](/python/langchain-classic/vectorstores/deeplake)[module

azure\_cosmos\_db](/python/langchain-classic/vectorstores/azure_cosmos_db)[module

astradb](/python/langchain-classic/vectorstores/astradb)[module

sklearn](/python/langchain-classic/vectorstores/sklearn)[module

alibabacloud\_opensearch](/python/langchain-classic/vectorstores/alibabacloud_opensearch)[module

yellowbrick](/python/langchain-classic/vectorstores/yellowbrick)[module

vald](/python/langchain-classic/vectorstores/vald)[module

bageldb](/python/langchain-classic/vectorstores/bageldb)[module

elastic\_vector\_search](/python/langchain-classic/vectorstores/elastic_vector_search)[module

awadb](/python/langchain-classic/vectorstores/awadb)[module

redis](/python/langchain-classic/vectorstores/redis)[module

docarray](/python/langchain-classic/vectorstores/docarray)


