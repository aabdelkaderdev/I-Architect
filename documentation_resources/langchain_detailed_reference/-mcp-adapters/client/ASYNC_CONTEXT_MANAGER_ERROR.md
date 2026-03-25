<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/client/ASYNC_CONTEXT_MANAGER_ERROR -->

Attributev0.2.2 (latest)●Since v0.1

# ASYNC\_CONTEXT\_MANAGER\_ERROR


```
ASYNC_CONTEXT_MANAGER_ERROR = 'As of langchain-mcp-adapters 0.1.0, MultiServerMCPClient cannot be used as a context manager (
  e.g.,
  async with MultiServerMCPClient(...)). Instead, you can do one of the following:\n1. client = MultiServerMCPClient(...)\n   tools = await client.get_tools()\n2. client = MultiServerMCPClient(...)\n   async with client.session(server_name) as session:\n       tools = await load_mcp_tools(session
)'
```


