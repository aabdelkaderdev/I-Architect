<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/shell_tool/DEFAULT_TOOL_DESCRIPTION -->

Attributev1.2.13 (latest)●Since v1.0

# DEFAULT\_TOOL\_DESCRIPTION


```
DEFAULT_TOOL_DESCRIPTION = 'Execute a shell command inside a persistent session. Before running a command, confirm the working directory is correct (
  e.g.,
  inspect with `ls` or `pwd`
) and ensure any parent directories exist. Prefer absolute paths and quote paths containing spaces, such as `cd "/path/with spaces"`. Chain multiple commands with `&&` or `;` instead of embedding newlines. Avoid unnecessary `cd` usage unless explicitly required so the session remains stable. Outputs may be truncated when they become very large, and long running commands will be terminated once their configured timeout elapses.'
```


