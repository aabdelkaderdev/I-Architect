<!-- Source: https://reference.langchain.com/python/langchain-community/chat_message_histories -->

Modulev0.4.1 (latest)●Since v0.3

# chat\_message\_histories

**Chat message history** stores a history of the message interactions in a chat.

**Class hierarchy:**

.. code-block::

```
BaseChatMessageHistory --> <name>ChatMessageHistory  # Examples: FileChatMessageHistory, PostgresChatMessageHistory
```

**Main helpers:**

.. code-block::

```
AIMessage, HumanMessage, BaseMessage
```

## Classes

[class

CassandraChatMessageHistory

Chat message history that is backed by Cassandra.](/python/langchain-community/chat_message_histories/cassandra/CassandraChatMessageHistory)[class

CosmosDBChatMessageHistory

Chat message history backed by Azure CosmosDB.](/python/langchain-community/chat_message_histories/cosmos_db/CosmosDBChatMessageHistory)[class

DynamoDBChatMessageHistory

Chat message history that stores history in AWS DynamoDB.

This class expects that a DynamoDB table exists with name `table_name`](/python/langchain-community/chat_message_histories/dynamodb/DynamoDBChatMessageHistory)[class

FileChatMessageHistory

Chat message history that stores history in a local file.](/python/langchain-community/chat_message_histories/file/FileChatMessageHistory)[class

FirestoreChatMessageHistory

Chat message history backed by Google Firestore.](/python/langchain-community/chat_message_histories/firestore/FirestoreChatMessageHistory)[class

KafkaChatMessageHistory

Chat message history stored in Kafka.](/python/langchain-community/chat_message_histories/kafka/KafkaChatMessageHistory)[class

MomentoChatMessageHistory

Chat message history cache that uses Momento as a backend.

See <https://gomomento.com/>](/python/langchain-community/chat_message_histories/momento/MomentoChatMessageHistory)[class

RedisChatMessageHistory

Chat message history stored in a Redis database.](/python/langchain-community/chat_message_histories/redis/RedisChatMessageHistory)[class

RocksetChatMessageHistory

Uses Rockset to store chat messages.

To use, ensure that the `rockset` python package installed.](/python/langchain-community/chat_message_histories/rocksetdb/RocksetChatMessageHistory)[class

SQLChatMessageHistory

Chat message history stored in an SQL database.](/python/langchain-community/chat_message_histories/sql/SQLChatMessageHistory)[class

StreamlitChatMessageHistory

Chat message history that stores messages in Streamlit session state.](/python/langchain-community/chat_message_histories/streamlit/StreamlitChatMessageHistory)[class

TiDBChatMessageHistory

Represents a chat message history stored in a TiDB database.](/python/langchain-community/chat_message_histories/tidb/TiDBChatMessageHistory)[class

UpstashRedisChatMessageHistory

Chat message history stored in an Upstash Redis database.](/python/langchain-community/chat_message_histories/upstash_redis/UpstashRedisChatMessageHistory)[class

XataChatMessageHistory

Chat message history stored in a Xata database.](/python/langchain-community/chat_message_histories/xata/XataChatMessageHistory)[class

ZepChatMessageHistory

Chat message history that uses Zep as a backend.

Recommended usage::

```
# Set up Zep Chat History
zep_chat_history = ZepChatMessageHistory(
    session_id=session_id,
    url=ZEP_API_URL,
    api_key=<your_api_key>,
)

# Use a standard ConversationBufferMemory to encapsulate the Zep chat history
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=zep_chat_history
)
```

Zep provides long-term conversation storage for LLM apps. The server stores,
summarizes, embeds, indexes, and enriches conversational AI chat
histories, and exposes them via simple, low-latency APIs.

For server installation instructions and more, see:
<https://docs.getzep.com/deployment/quickstart/>

This class is a thin wrapper around the zep-python package. Additional
Zep functionality is exposed via the `zep_summary` and `zep_messages`
properties.

For more information on the zep-python package, see:
<https://github.com/getzep/zep-python>](/python/langchain-community/chat_message_histories/zep/ZepChatMessageHistory)[class

ZepCloudChatMessageHistory

Chat message history that uses Zep Cloud as a backend.

Recommended usage::

```
# Set up Zep Chat History
zep_chat_history = ZepChatMessageHistory(
    session_id=session_id,
    api_key=<your_api_key>,
)

# Use a standard ConversationBufferMemory to encapsulate the Zep chat history
memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=zep_chat_history
)
```

Zep - Recall, understand, and extract data from chat histories.
Power personalized AI experiences.

Zep is a long-term memory service for AI Assistant apps.
With Zep, you can provide AI assistants with the
ability to recall past conversations,
no matter how distant,
while also reducing hallucinations, latency, and cost.

see Zep Cloud Docs: <https://help.getzep.com>

This class is a thin wrapper around the zep-python package. Additional
Zep functionality is exposed via the `zep_summary`, `zep_messages` and `zep_facts`
properties.

For more information on the zep-python package, see:
<https://github.com/getzep/zep-python>](/python/langchain-community/chat_message_histories/zep_cloud/ZepCloudChatMessageHistory)[deprecatedclass

ElasticsearchChatMessageHistory

Chat message history that stores history in Elasticsearch.](/python/langchain-community/chat_message_histories/elasticsearch/ElasticsearchChatMessageHistory)[deprecatedclass

PostgresChatMessageHistory

Chat message history stored in a Postgres database.

**DEPRECATED**: This class is deprecated and will be removed in a future version.

Use the `PostgresChatMessageHistory` implementation in `langchain_postgres`.](/python/langchain-community/chat_message_histories/postgres/PostgresChatMessageHistory)[deprecatedclass

SingleStoreDBChatMessageHistory

Chat message history stored in a SingleStoreDB database.](/python/langchain-community/chat_message_histories/singlestoredb/SingleStoreDBChatMessageHistory)

## Modules

[module

xata](/python/langchain-community/chat_message_histories/xata)[module

redis](/python/langchain-community/chat_message_histories/redis)[module

cassandra

Cassandra-based chat message history, based on cassIO.](/python/langchain-community/chat_message_histories/cassandra)[module

in\_memory](/python/langchain-community/chat_message_histories/in_memory)[module

zep](/python/langchain-community/chat_message_histories/zep)[module

dynamodb](/python/langchain-community/chat_message_histories/dynamodb)[module

rocksetdb](/python/langchain-community/chat_message_histories/rocksetdb)[module

sql](/python/langchain-community/chat_message_histories/sql)[module

upstash\_redis](/python/langchain-community/chat_message_histories/upstash_redis)[module

singlestoredb](/python/langchain-community/chat_message_histories/singlestoredb)[module

kafka

Kafka-based chat message history by using confluent-kafka-python.
confluent-kafka-python is under Apache 2.0 license.
<https://github.com/confluentinc/confluent-kafka-python>](/python/langchain-community/chat_message_histories/kafka)[module

postgres](/python/langchain-community/chat_message_histories/postgres)[module

firestore

Firestore Chat Message History.](/python/langchain-community/chat_message_histories/firestore)[module

tidb](/python/langchain-community/chat_message_histories/tidb)[module

zep\_cloud](/python/langchain-community/chat_message_histories/zep_cloud)[module

elasticsearch](/python/langchain-community/chat_message_histories/elasticsearch)[module

momento](/python/langchain-community/chat_message_histories/momento)[module

cosmos\_db

Azure CosmosDB Memory History.](/python/langchain-community/chat_message_histories/cosmos_db)[module

file](/python/langchain-community/chat_message_histories/file)[module

streamlit](/python/langchain-community/chat_message_histories/streamlit)


