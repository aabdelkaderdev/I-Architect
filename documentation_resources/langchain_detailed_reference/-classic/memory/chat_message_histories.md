<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/chat_message_histories -->

Modulev1.2.13 (latest)●Since v1.0

# chat\_message\_histories

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/memory/chat_message_histories/DEPRECATED_LOOKUP)

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

xata](/python/langchain-classic/memory/chat_message_histories/xata)[module

redis](/python/langchain-classic/memory/chat_message_histories/redis)[module

cassandra](/python/langchain-classic/memory/chat_message_histories/cassandra)[module

in\_memory](/python/langchain-classic/memory/chat_message_histories/in_memory)[module

zep](/python/langchain-classic/memory/chat_message_histories/zep)[module

dynamodb](/python/langchain-classic/memory/chat_message_histories/dynamodb)[module

rocksetdb](/python/langchain-classic/memory/chat_message_histories/rocksetdb)[module

sql](/python/langchain-classic/memory/chat_message_histories/sql)[module

upstash\_redis](/python/langchain-classic/memory/chat_message_histories/upstash_redis)[module

singlestoredb](/python/langchain-classic/memory/chat_message_histories/singlestoredb)[module

mongodb](/python/langchain-classic/memory/chat_message_histories/mongodb)[module

postgres](/python/langchain-classic/memory/chat_message_histories/postgres)[module

firestore](/python/langchain-classic/memory/chat_message_histories/firestore)[module

elasticsearch](/python/langchain-classic/memory/chat_message_histories/elasticsearch)[module

momento](/python/langchain-classic/memory/chat_message_histories/momento)[module

cosmos\_db](/python/langchain-classic/memory/chat_message_histories/cosmos_db)[module

file](/python/langchain-classic/memory/chat_message_histories/file)[module

astradb](/python/langchain-classic/memory/chat_message_histories/astradb)[module

streamlit](/python/langchain-classic/memory/chat_message_histories/streamlit)[module

neo4j](/python/langchain-classic/memory/chat_message_histories/neo4j)


