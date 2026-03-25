<!-- Source: https://docs.langchain.com/oss/python/integrations/chat_message_histories/cockroachdb -->

`CockroachDBChatMessageHistory` stores chat conversation history in CockroachDB’s distributed SQL database.
The code lives in the integration package: [langchain-cockroachdb](https://github.com/cockroachdb/langchain-cockroachdb/).

## [​](#overview) Overview

CockroachDBChatMessageHistory provides:

- **Distributed storage**: Chat history automatically replicated across nodes
- **Strong consistency**: SERIALIZABLE transactions prevent message ordering issues
- **High availability**: Automatic failover with no data loss
- **Session isolation**: Each conversation has a unique session ID
- **PostgreSQL compatibility**: Easy migration from PostgreSQL-based systems

## [​](#setup) Setup

### [​](#install) Install

Copy

```
pip install -qU langchain-cockroachdb
```

### [​](#connection-string) Connection string

Copy

```
# CockroachDB Cloud
CONNECTION_STRING = "cockroachdb://user:password@host:26257/database?sslmode=verify-full"

# Local insecure cluster  
CONNECTION_STRING = "cockroachdb://root@localhost:26257/defaultdb?sslmode=disable"
```

## [​](#initialization) Initialization

### [​](#create-the-message-history-table) Create the message history table

Copy

```
import asyncio
from langchain_cockroachdb import CockroachDBChatMessageHistory

# Create table (only needs to be done once)
async def setup():
    chat_history = CockroachDBChatMessageHistory(
        session_id="setup",
        connection_string=CONNECTION_STRING,
        table_name="chat_history",
    )
    await chat_history._acreate_table_if_not_exists()

asyncio.run(setup())
```

**Optional**: Specify a schema name by using `schema` parameter (default: “public”)

### [​](#initialize-for-a-session) Initialize for a session

Create a chat history instance for a specific conversation:

Copy

```
import uuid

session_id = str(uuid.uuid4())  # Unique ID for this conversation

chat_history = CockroachDBChatMessageHistory(
    session_id=session_id,
    connection_string=CONNECTION_STRING,
    table_name="chat_history",
)
```

## [​](#usage) Usage

### [​](#add-messages) Add messages

Copy

```
from langchain.messages import HumanMessage, AIMessage

# Add messages to the conversation
await chat_history.aadd_message(HumanMessage(content="Hello! What is CockroachDB?"))
await chat_history.aadd_message(AIMessage(content="CockroachDB is a distributed SQL database..."))
```

### [​](#add-multiple-messages-at-once) Add multiple messages at once

Copy

```
messages = [
    HumanMessage(content="What are vector indexes?"),
    AIMessage(content="Vector indexes enable fast similarity search..."),
    HumanMessage(content="How do they work?"),
    AIMessage(content="They use approximate nearest neighbor algorithms..."),
]

await chat_history.aadd_messages(messages)
```

### [​](#retrieve-messages) Retrieve messages

Get all messages for the session:

Copy

```
messages = await chat_history.aget_messages()

for msg in messages:
    if isinstance(msg, HumanMessage):
        print(f"User: {msg.content}")
    elif isinstance(msg, AIMessage):
        print(f"AI: {msg.content}")
```

### [​](#clear-conversation-history) Clear conversation history

Delete all messages for the session:

Copy

```
await chat_history.aclear()
```

## [​](#sync-interface) Sync interface

Use the synchronous API:

Copy

```
# Sync usage
chat_history_sync = CockroachDBChatMessageHistory(
    session_id=session_id,
    connection_string=CONNECTION_STRING,
    table_name="chat_history",
)

# Sync operations
chat_history_sync.add_message(HumanMessage(content="Hello!"))
messages = chat_history_sync.messages
chat_history_sync.clear()
```

## [​](#api-reference) API reference

For detailed documentation:

- [GitHub repository](https://github.com/cockroachdb/langchain-cockroachdb)
- [PyPI package](https://pypi.org/project/langchain-cockroachdb/)

## [​](#additional-resources) Additional resources

- [CockroachDB documentation](https://www.cockroachlabs.com/docs/)
- [CockroachDB Cloud](https://cockroachlabs.cloud)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat_message_histories/cockroachdb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.