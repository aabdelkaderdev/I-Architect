<!-- Source: https://docs.trychroma.com/integrations/frameworks/anthropic-mcp -->

## [​](#what-is-mcp) What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications communicate with data sources and tools. Think of MCP like a USB-C port for AI applications - it provides a universal way to connect AI models like Claude to different services and data sources.
MCP follows a client-server architecture:

- **MCP Hosts**: Applications like Claude Desktop that want to access data through MCP
- **MCP Clients**: Protocol clients that maintain connections with servers
- **MCP Servers**: Lightweight programs that expose specific capabilities (like Chroma)
- **Data Sources**: Your local or remote data that MCP servers can securely access

## [​](#what-is-the-chroma-mcp-server) What is the Chroma MCP Server?

The Chroma MCP server allows Claude to directly interact with Chroma’s search capabilities through this standardized protocol. This enables powerful features like:

- Persistent memory across conversations
- Semantic search through previous chats
- Document management and retrieval
- Vector and keyword search capabilities
- Metadata management and filtering

## [​](#prerequisites) Prerequisites

Before setting up the Chroma MCP server, ensure you have:

1. Claude Desktop installed (Windows or macOS)
2. Python 3.10+ installed
3. `uvx` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## [​](#setup-guide) Setup Guide

### [​](#1-configure-mcp-server) 1. Configure MCP Server

1. Open Claude Desktop
2. Click on the Claude menu and select “Settings…”
3. Click on “Developer” in the left sidebar
4. Click “Edit Config” to open your configuration file

Add the following configuration:

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        "/path/to/your/data/directory"
      ]
    }
  }
}
```

Replace `/path/to/your/data/directory` with where you want Chroma to store its data, for example:

- macOS: `/Users/username/Documents/chroma-data`
- Windows: `C:\\Users\\username\\Documents\\chroma-data`

### [​](#2-restart-and-verify) 2. Restart and Verify

1. Restart Claude Desktop completely
2. Look for the hammer icon in the bottom right of your chat input
3. Click it to see available Chroma tools

If you don’t see the tools, check the logs at:

- macOS: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\logs\mcp*.log`

## [​](#client-types) Client Types

The Chroma MCP server supports multiple client types to suit different needs:

### [​](#1-ephemeral-client-default) 1. Ephemeral Client (Default)

By default, the server will use the ephemeral client.

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
      ]
    }
  }
}
```

- Stores data in memory only
- Data is cleared when the server restarts
- Useful for temporary sessions or testing

### [​](#2-persistent-client) 2. Persistent Client

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        "/path/to/your/data/directory"
      ]
    }
  }
}
```

- Stores data persistently on your local machine
- Data survives between restarts
- Best for personal use and long-term memory

### [​](#3-self-hosted-client) 3. Self-Hosted Client

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "http",
        "--host",
        "http://localhost:8000",
        "--port",
        "8000",
        "--custom-auth-credentials",
        "username:password",
        "--ssl",
        "true"
      ]
    }
  }
}
```

- Connects to your own Chroma server
- Full control over data and infrastructure
- Suitable for team environments

### [​](#4-cloud-client) 4. Cloud Client

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "cloud",
        "--tenant",
        "your-tenant-id",
        "--database",
        "your-database-name",
        "--api-key",
        "your-api-key"
      ]
    }
  }
}
```

- Connects to Chroma Cloud or other hosted instances
- Scalable and managed infrastructure
- Best for production deployments

## [​](#using-chroma-with-claude) Using Chroma with Claude

### [​](#team-knowledge-base-example) Team Knowledge Base Example

Let’s say your team maintains a knowledge base of customer support interactions. By storing these in Chroma Cloud, team members can use Claude to quickly access and learn from past support cases.
First, set up your shared knowledge base:

Report incorrect code

Copy

Ask AI

```
import chromadb
from datetime import datetime

# Connect to Chroma Cloud
client = chromadb.HttpClient(
    ssl=True,
    host='api.trychroma.com',
    tenant='your-tenant-id',
    database='support-kb',
    headers={
        'x-chroma-token': 'YOUR_API_KEY'
    }
)

# Create a collection for support cases
collection = client.create_collection("support_cases")

# Add some example support cases
support_cases = [
    {
        "case": "Customer reported issues connecting their IoT devices to the dashboard.",
        "resolution": "Guided customer through firewall configuration and port forwarding setup.",
        "category": "connectivity",
        "date": "2024-03-15"
    },
    {
        "case": "User couldn't access admin features after recent update.",
        "resolution": "Discovered role permissions weren't migrated correctly. Applied fix and documented process.",
        "category": "permissions",
        "date": "2024-03-16"
    }
]

# Add documents to collection
collection.add(
    documents=[case["case"] + "\n" + case["resolution"] for case in support_cases],
    metadatas=[{
        "category": case["category"],
        "date": case["date"]
    } for case in support_cases],
    ids=[f"case_{i}" for i in range(len(support_cases))]
)
```

Now team members can use Claude to access this knowledge.
In your claude config, add the following:

Report incorrect code

Copy

Ask AI

```
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "cloud",
        "--tenant",
        "your-tenant-id",
        "--database",
        "support-kb",
        "--api-key",
        "YOUR_API_KEY"
      ]
    }
  }
}
```

Now you can use the knowledge base in your chats:

Report incorrect code

Copy

Ask AI

```
Claude, I'm having trouble helping a customer with IoT device connectivity.
Can you check our support knowledge base for similar cases and suggest a solution?
```

Claude will:

1. Search the shared knowledge base for relevant cases
2. Consider the context and solutions from similar past issues
3. Provide recommendations based on previous successful resolutions

This setup is particularly powerful because:

- All support team members have access to the same knowledge base
- Claude can learn from the entire team’s experience
- Solutions are standardized across the organization
- New team members can quickly get up to speed on common issues

### [​](#project-memory-example) Project Memory Example

Claude’s context window has limits - long conversations eventually get truncated, and chats don’t persist between sessions. Using Chroma as an external memory store solves these limitations, allowing Claude to reference past conversations and maintain context across multiple sessions.
First, tell Claude to use Chroma for memory as part of the project setup:

Report incorrect code

Copy

Ask AI

```
Remember, you have access to Chroma tools.
At any point if the user references previous chats or memory, check chroma for similar conversations.
Try to use retrieved information where possible.
```

This prompt instructs Claude to:

- Proactively check Chroma when memory-related topics come up
- Search for semantically similar past conversations
- Incorporate relevant historical context into responses

To store the current conversation:

Report incorrect code

Copy

Ask AI

```
Please chunk our conversation into small chunks and store it in Chroma for future reference.
```

Claude will:

1. Break the conversation into smaller chunks (typically 512-1024 tokens)
   - Chunking is necessary because:
   - Large texts are harder to search semantically
   - Smaller chunks help retrieve more precise context
   - It prevents token limits in future retrievals
2. Generate embeddings for each chunk
3. Add metadata like timestamps and detected topics
4. Store everything in your Chroma collection

Later, you can access past conversations naturally:

Report incorrect code

Copy

Ask AI

```
What did we discuss previously about the authentication system?
```

Claude will:

1. Search Chroma for chunks semantically related to authentication
2. Filter by timestamp metadata for last week’s discussions
3. Incorporate the relevant historical context into its response

This setup is particularly useful for:

- Long-running projects where context gets lost
- Teams where multiple people interact with Claude
- Complex discussions that reference past decisions
- Maintaining consistent context across multiple chat sessions

### [​](#advanced-features) Advanced Features

The Chroma MCP server supports:

- **Collection Management**: Create and organize separate collections for different projects
- **Document Operations**: Add, update, or delete documents
- **Search Capabilities**:
  - Vector similarity search
  - Keyword-based search
  - Metadata filtering
- **Batch Processing**: Efficient handling of multiple operations

## [​](#troubleshooting) Troubleshooting

If you encounter issues:

1. Verify your configuration file syntax
2. Ensure all paths are absolute and valid
3. Try using full paths for `uvx` with `which uvx` and using that path in the config
4. Check the Claude logs (paths listed above)

## [​](#resources) Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/introduction)
- [Chroma MCP Server Documentation](https://github.com/chroma-core/chroma-mcp)
- [Claude Desktop Guide](https://docs.anthropic.com/claude/docs/claude-desktop)