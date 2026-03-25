<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/file_search -->

Modulev1.2.13 (latest)●Since v1.0

# file\_search

File search middleware for Anthropic text editor and memory tools.

This module provides Glob and Grep search tools that operate on files stored
in state or filesystem.

## Attributes

[attribute

ResponseT](/python/langchain/agents/middleware/file_search/ResponseT)

## Classes

[class

AgentMiddleware

Base middleware class for an agent.

Subclass this and implement any of the defined methods to customize agent behavior
between steps in the main agent loop.](/python/langchain/agents/middleware/file_search/AgentMiddleware)[class

AgentState

State schema for the agent.](/python/langchain/agents/middleware/file_search/AgentState)[class

FilesystemFileSearchMiddleware

Provides Glob and Grep search over filesystem files.

This middleware adds two tools that search through local filesystem:

- Glob: Fast file pattern matching by file path
- Grep: Fast content search using ripgrep or Python fallback](/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware)


