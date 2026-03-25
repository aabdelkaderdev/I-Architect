<!-- Source: https://reference.langchain.com/python/langchain-mcp-adapters/sessions/StdioConnection/env -->

Attributev0.2.2 (latest)●Since v0.1

# env

The environment to use when spawning the process.

If not specified or set to None, a subset of the default environment
variables from the current process will be used.

Please refer to the MCP SDK documentation for details on which
environment variables are included by default. The behavior
varies by operating system.

<https://github.com/modelcontextprotocol/python-sdk/blob/c47c767ff437ee88a19e6b9001e2472cb6f7d5ed/src/mcp/client/stdio/__init__.py#L51>


```
env: NotRequired[dict[str, str] | None]
```


