<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware/__init__/glob_search -->

Functionv1.2.13 (latest)●Since v1.0

# glob\_search

Fast file pattern matching tool that works with any codebase size.

Supports glob patterns like `**/*.js` or `src/**/*.ts`.

Returns matching file paths sorted by modification time.

Use this tool when you need to find files by name patterns.


```
glob_search(
    pattern: str,
    path: str = '/',
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pattern`\* | `str` | The glob pattern to match files against. |
| `path` | `str` | Default:`'/'`  The directory to search in. If not specified, searches from root. |


