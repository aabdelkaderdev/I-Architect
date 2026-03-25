<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware/__init__/grep_search -->

Functionv1.2.13 (latest)●Since v1.0

# grep\_search

Fast content search tool that works with any codebase size.

Searches file contents using regular expressions. Supports full regex
syntax and filters files by pattern with the include parameter.


```
grep_search(
  pattern: str,
  path: str = '/',
  include: str | None = None,
  output_mode: Literal['files_with_matches', 'content', 'count'] = 'files_with_matches'
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `pattern`\* | `str` | The regular expression pattern to search for in file contents. |
| `path` | `str` | Default:`'/'`  The directory to search in. If not specified, searches from root. |
| `include` | `str | None` | Default:`None`  File pattern to filter (e.g., `'*.js'`, `'*.{ts,tsx}'`). |
| `output_mode` | `Literal['files_with_matches', 'content', 'count']` | Default:`'files_with_matches'`  Output format:   - `'files_with_matches'`: Only file paths containing matches - `'content'`: Matching lines with `file:line:content` format - `'count'`: Count of matches per file |


