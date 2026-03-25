<!-- Source: https://docs.trychroma.com/integrations/frameworks/google-adk -->

The [Agent Development Kit (ADK)](https://google.github.io/adk-docs/) is Google’s open-source framework for building AI agents. Chroma integrates with ADK via the [Chroma MCP server](https://github.com/chroma-core/chroma-mcp), giving your agents access to semantic memory, knowledge base retrieval, and persistent context across sessions.

- Python
- TypeScript

## [​](#prerequisites) Prerequisites

- Python 3.10+
- `uvx` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## [​](#setup) Setup

- Chroma Cloud
- Local

[Chroma Cloud](https://trychroma.com/signup?utm_source=docs-adk) is a fully managed, serverless database-as-a-service. Get started in 30 seconds - $5 in free credits included.

1

### Install and log in

pip

uv

Report incorrect code

Copy

Ask AI

```
pip install chromadb google-adk
```

Then authenticate with Chroma Cloud:

Report incorrect code

Copy

Ask AI

```
chroma login
```

2

### Create a database

Report incorrect code

Copy

Ask AI

```
chroma db create my-adk-db
```

3

### Get your connection variables

Report incorrect code

Copy

Ask AI

```
chroma db connect my-adk-db --env-vars
```

This will output your `CHROMA_TENANT`, `CHROMA_DATABASE`, and `CHROMA_API_KEY`. Use them in the code below.

4

### Create your agent

Python

Report incorrect code

Copy

Ask AI

```
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

CHROMA_TENANT = "your-tenant-id"
CHROMA_DATABASE = "my-adk-db"
CHROMA_API_KEY = "your-api-key"

root_agent = Agent(
    model="gemini-2.5-pro",
    name="chroma_agent",
    instruction="Help users store and retrieve information using semantic search.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=[
                        "chroma-mcp",
                        "--client-type", "cloud",
                        "--tenant", CHROMA_TENANT,
                        "--database", CHROMA_DATABASE,
                        "--api-key", CHROMA_API_KEY,
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
```

## [​](#example-semantic-memory-agent) Example: Semantic Memory Agent

This example builds a personal assistant that uses Chroma as a persistent semantic memory store. The agent remembers facts from past conversations — user preferences, project context, decisions — and recalls them when relevant.The agent’s instruction tells it to create a Chroma collection for storing memories, and to use it for storage and retrieval:

Python

Report incorrect code

Copy

Ask AI

```
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

CHROMA_TENANT = "your-tenant-id"
CHROMA_DATABASE = "my-adk-db"
CHROMA_API_KEY = "your-api-key"

MEMORY_INSTRUCTION = """You are a personal assistant with persistent memory.

You have access to Chroma tools for managing collections and documents.

## First run
On your first interaction, use chroma_create_collection to create a collection
called "memory". If it already exists, that's fine — just use the existing one.

## Storing memories
When the user shares important information — preferences, project details,
decisions, or personal context — store it in the "memory" collection using
chroma_add_documents. Each memory should be a concise, self-contained fact.
Tag memories with metadata like {"type": "preference"}, {"type": "fact"},
or {"type": "decision"} so they can be filtered later.

## Recalling memories
At the start of a conversation, or when the user asks about something that
might relate to past context, use chroma_query_documents to search the
"memory" collection. Use the results to inform your responses without
the user having to repeat themselves.

## Memory hygiene
If the user corrects a previous fact, use chroma_update_documents to update
the old memory rather than creating a duplicate.
"""

root_agent = Agent(
    model="gemini-2.5-pro",
    name="memory_agent",
    instruction=MEMORY_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=[
                        "chroma-mcp",
                        "--client-type", "cloud",
                        "--tenant", CHROMA_TENANT,
                        "--database", CHROMA_DATABASE,
                        "--api-key", CHROMA_API_KEY,
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
```

With this setup, a conversation might look like:

Report incorrect code

Copy

Ask AI

```
User: I'm working on Project Atlas — it's a migration from PostgreSQL to
      DynamoDB. Our deadline is end of Q3 and the team lead is Sarah.

Agent: Got it, I've stored those project details. I'll remember them for
       future conversations.
       (creates "memory" collection, stores 3 memories: project description,
       deadline, team lead)

--- later session ---

User: What do you remember about my current project?

Agent: You're working on Project Atlas — a PostgreSQL to DynamoDB migration.
       Sarah is the team lead and your deadline is end of Q3.
       (retrieved via semantic search on "current project")
```

For a more in-depth look at building agentic memory with Chroma, see the [Agentic Memory guide](/guides/build/agentic-memory).

Install the dependencies:

pip

uv

Report incorrect code

Copy

Ask AI

```
pip install chromadb google-adk
```

Replace `/path/to/your/data/directory` with where you want Chroma to store its data.

Python

Report incorrect code

Copy

Ask AI

```
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

DATA_DIR = "/path/to/your/data/directory"

root_agent = Agent(
    model="gemini-2.5-pro",
    name="chroma_agent",
    instruction="Help users store and retrieve information using semantic search.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=[
                        "chroma-mcp",
                        "--client-type", "persistent",
                        "--data-dir", DATA_DIR,
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
```

## [​](#example-semantic-memory-agent-2) Example: Semantic Memory Agent

This example builds a personal assistant that uses Chroma as a persistent semantic memory store. The agent remembers facts from past conversations — user preferences, project context, decisions — and recalls them when relevant.The agent’s instruction tells it to create a Chroma collection for storing memories, and to use it for storage and retrieval:

Python

Report incorrect code

Copy

Ask AI

```
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

DATA_DIR = "/path/to/your/data/directory"

MEMORY_INSTRUCTION = """You are a personal assistant with persistent memory.

You have access to Chroma tools for managing collections and documents.

## First run
On your first interaction, use chroma_create_collection to create a collection
called "memory". If it already exists, that's fine — just use the existing one.

## Storing memories
When the user shares important information — preferences, project details,
decisions, or personal context — store it in the "memory" collection using
chroma_add_documents. Each memory should be a concise, self-contained fact.
Tag memories with metadata like {"type": "preference"}, {"type": "fact"},
or {"type": "decision"} so they can be filtered later.

## Recalling memories
At the start of a conversation, or when the user asks about something that
might relate to past context, use chroma_query_documents to search the
"memory" collection. Use the results to inform your responses without
the user having to repeat themselves.

## Memory hygiene
If the user corrects a previous fact, use chroma_update_documents to update
the old memory rather than creating a duplicate.
"""

root_agent = Agent(
    model="gemini-2.5-pro",
    name="memory_agent",
    instruction=MEMORY_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=[
                        "chroma-mcp",
                        "--client-type", "persistent",
                        "--data-dir", DATA_DIR,
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
```

With this setup, a conversation might look like:

Report incorrect code

Copy

Ask AI

```
User: I'm working on Project Atlas — it's a migration from PostgreSQL to
      DynamoDB. Our deadline is end of Q3 and the team lead is Sarah.

Agent: Got it, I've stored those project details. I'll remember them for
       future conversations.
       (creates "memory" collection, stores 3 memories: project description,
       deadline, team lead)

--- later session ---

User: What do you remember about my current project?

Agent: You're working on Project Atlas — a PostgreSQL to DynamoDB migration.
       Sarah is the team lead and your deadline is end of Q3.
       (retrieved via semantic search on "current project")
```

For a more in-depth look at building agentic memory with Chroma, see the [Agentic Memory guide](/guides/build/agentic-memory).

## [​](#prerequisites-2) Prerequisites

- Node.js 18+
- `uvx` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## [​](#setup-2) Setup

- Chroma Cloud
- Local

[Chroma Cloud](https://trychroma.com/signup?utm_source=docs-adk) is a fully managed, serverless database-as-a-service. Get started in 30 seconds - $5 in free credits included.

1

### Install and log in

Install the ADK package:

npm

pnpm

yarn

Report incorrect code

Copy

Ask AI

```
npm install @google/adk
```

Install the Chroma CLI and authenticate:

pip

uv

Report incorrect code

Copy

Ask AI

```
pip install chromadb
```

Report incorrect code

Copy

Ask AI

```
chroma login
```

2

### Create a database

Report incorrect code

Copy

Ask AI

```
chroma db create my-adk-db
```

3

### Get your connection variables

Report incorrect code

Copy

Ask AI

```
chroma db connect my-adk-db --env-vars
```

This will output your `CHROMA_TENANT`, `CHROMA_DATABASE`, and `CHROMA_API_KEY`. Use them in the code below.

4

### Create your agent

TypeScript

Report incorrect code

Copy

Ask AI

```
import { LlmAgent, MCPToolset } from "@google/adk";

const CHROMA_TENANT = "your-tenant-id";
const CHROMA_DATABASE = "my-adk-db";
const CHROMA_API_KEY = "your-api-key";

const rootAgent = new LlmAgent({
    model: "gemini-2.5-pro",
    name: "chroma_agent",
    instruction: "Help users store and retrieve information using semantic search.",
    tools: [
        new MCPToolset({
            type: "StdioConnectionParams",
            serverParams: {
                command: "uvx",
                args: [
                    "chroma-mcp",
                    "--client-type", "cloud",
                    "--tenant", CHROMA_TENANT,
                    "--database", CHROMA_DATABASE,
                    "--api-key", CHROMA_API_KEY,
                ],
            },
        }),
    ],
});
```

## [​](#example-semantic-memory-agent-3) Example: Semantic Memory Agent

This example builds a personal assistant that uses Chroma as a persistent semantic memory store. The agent remembers facts from past conversations — user preferences, project context, decisions — and recalls them when relevant.The agent’s instruction tells it to create a Chroma collection for storing memories, and to use it for storage and retrieval:

TypeScript

Report incorrect code

Copy

Ask AI

```
import { LlmAgent, MCPToolset } from "@google/adk";

const CHROMA_TENANT = "your-tenant-id";
const CHROMA_DATABASE = "my-adk-db";
const CHROMA_API_KEY = "your-api-key";

const MEMORY_INSTRUCTION = `You are a personal assistant with persistent memory.

You have access to Chroma tools for managing collections and documents.

## First run
On your first interaction, use chroma_create_collection to create a collection
called "memory". If it already exists, that's fine — just use the existing one.

## Storing memories
When the user shares important information — preferences, project details,
decisions, or personal context — store it in the "memory" collection using
chroma_add_documents. Each memory should be a concise, self-contained fact.
Tag memories with metadata like {"type": "preference"}, {"type": "fact"},
or {"type": "decision"} so they can be filtered later.

## Recalling memories
At the start of a conversation, or when the user asks about something that
might relate to past context, use chroma_query_documents to search the
"memory" collection. Use the results to inform your responses without
the user having to repeat themselves.

## Memory hygiene
If the user corrects a previous fact, use chroma_update_documents to update
the old memory rather than creating a duplicate.
`;

const rootAgent = new LlmAgent({
    model: "gemini-2.5-pro",
    name: "memory_agent",
    instruction: MEMORY_INSTRUCTION,
    tools: [
        new MCPToolset({
            type: "StdioConnectionParams",
            serverParams: {
                command: "uvx",
                args: [
                    "chroma-mcp",
                    "--client-type", "cloud",
                    "--tenant", CHROMA_TENANT,
                    "--database", CHROMA_DATABASE,
                    "--api-key", CHROMA_API_KEY,
                ],
            },
        }),
    ],
});
```

With this setup, a conversation might look like:

Report incorrect code

Copy

Ask AI

```
User: I'm working on Project Atlas — it's a migration from PostgreSQL to
      DynamoDB. Our deadline is end of Q3 and the team lead is Sarah.

Agent: Got it, I've stored those project details. I'll remember them for
       future conversations.
       (creates "memory" collection, stores 3 memories: project description,
       deadline, team lead)

--- later session ---

User: What do you remember about my current project?

Agent: You're working on Project Atlas — a PostgreSQL to DynamoDB migration.
       Sarah is the team lead and your deadline is end of Q3.
       (retrieved via semantic search on "current project")
```

For a more in-depth look at building agentic memory with Chroma, see the [Agentic Memory guide](/guides/build/agentic-memory).

Install the ADK package:

npm

pnpm

yarn

Report incorrect code

Copy

Ask AI

```
npm install @google/adk
```

Replace `/path/to/your/data/directory` with where you want Chroma to store its data.

TypeScript

Report incorrect code

Copy

Ask AI

```
import { LlmAgent, MCPToolset } from "@google/adk";

const DATA_DIR = "/path/to/your/data/directory";

const rootAgent = new LlmAgent({
    model: "gemini-2.5-pro",
    name: "chroma_agent",
    instruction: "Help users store and retrieve information using semantic search.",
    tools: [
        new MCPToolset({
            type: "StdioConnectionParams",
            serverParams: {
                command: "uvx",
                args: [
                    "chroma-mcp",
                    "--client-type", "persistent",
                    "--data-dir", DATA_DIR,
                ],
            },
        }),
    ],
});
```

## [​](#example-semantic-memory-agent-4) Example: Semantic Memory Agent

This example builds a personal assistant that uses Chroma as a persistent semantic memory store. The agent remembers facts from past conversations — user preferences, project context, decisions — and recalls them when relevant.The agent’s instruction tells it to create a Chroma collection for storing memories, and to use it for storage and retrieval:

TypeScript

Report incorrect code

Copy

Ask AI

```
import { LlmAgent, MCPToolset } from "@google/adk";

const DATA_DIR = "/path/to/your/data/directory";

const MEMORY_INSTRUCTION = `You are a personal assistant with persistent memory.

You have access to Chroma tools for managing collections and documents.

## First run
On your first interaction, use chroma_create_collection to create a collection
called "memory". If it already exists, that's fine — just use the existing one.

## Storing memories
When the user shares important information — preferences, project details,
decisions, or personal context — store it in the "memory" collection using
chroma_add_documents. Each memory should be a concise, self-contained fact.
Tag memories with metadata like {"type": "preference"}, {"type": "fact"},
or {"type": "decision"} so they can be filtered later.

## Recalling memories
At the start of a conversation, or when the user asks about something that
might relate to past context, use chroma_query_documents to search the
"memory" collection. Use the results to inform your responses without
the user having to repeat themselves.

## Memory hygiene
If the user corrects a previous fact, use chroma_update_documents to update
the old memory rather than creating a duplicate.
`;

const rootAgent = new LlmAgent({
    model: "gemini-2.5-pro",
    name: "memory_agent",
    instruction: MEMORY_INSTRUCTION,
    tools: [
        new MCPToolset({
            type: "StdioConnectionParams",
            serverParams: {
                command: "uvx",
                args: [
                    "chroma-mcp",
                    "--client-type", "persistent",
                    "--data-dir", DATA_DIR,
                ],
            },
        }),
    ],
});
```

With this setup, a conversation might look like:

Report incorrect code

Copy

Ask AI

```
User: I'm working on Project Atlas — it's a migration from PostgreSQL to
      DynamoDB. Our deadline is end of Q3 and the team lead is Sarah.

Agent: Got it, I've stored those project details. I'll remember them for
       future conversations.
       (creates "memory" collection, stores 3 memories: project description,
       deadline, team lead)

--- later session ---

User: What do you remember about my current project?

Agent: You're working on Project Atlas — a PostgreSQL to DynamoDB migration.
       Sarah is the team lead and your deadline is end of Q3.
       (retrieved via semantic search on "current project")
```

For a more in-depth look at building agentic memory with Chroma, see the [Agentic Memory guide](/guides/build/agentic-memory).

## [​](#available-tools) Available Tools

Once connected, your ADK agent will have access to the following Chroma tools:

### [​](#collection-management) Collection Management

| Tool | Description |
| --- | --- |
| `chroma_list_collections` | List all collections with pagination support |
| `chroma_create_collection` | Create a new collection with optional HNSW configuration |
| `chroma_get_collection_info` | Get detailed information about a collection |
| `chroma_get_collection_count` | Get the number of documents in a collection |
| `chroma_modify_collection` | Update a collection’s name or metadata |
| `chroma_delete_collection` | Delete a collection |
| `chroma_peek_collection` | View a sample of documents in a collection |

### [​](#document-operations) Document Operations

| Tool | Description |
| --- | --- |
| `chroma_add_documents` | Add documents with optional metadata and custom IDs |
| `chroma_query_documents` | Query documents using semantic search with advanced filtering |
| `chroma_get_documents` | Retrieve documents by IDs or filters with pagination |
| `chroma_update_documents` | Update existing documents’ content, metadata, or embeddings |
| `chroma_delete_documents` | Delete specific documents from a collection |

## [​](#resources) Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Chroma Integration Guide](https://google.github.io/adk-docs/integrations/chroma/)
- [Chroma MCP Server](https://github.com/chroma-core/chroma-mcp)