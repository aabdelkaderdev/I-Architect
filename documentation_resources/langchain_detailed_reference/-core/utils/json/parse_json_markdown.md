<!-- Source: https://reference.langchain.com/python/langchain-core/utils/json/parse_json_markdown -->

Functionv1.2.21 (latest)●Since v0.1

# parse\_json\_markdown

Parse a JSON string from a Markdown string.


```
parse_json_markdown(
  json_string: str,
  *,
  parser: Callable[[str], Any] = parse_partial_json
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `json_string`\* | `str` | The Markdown string. |
| `parser` | `Callable[[str], Any]` | Default:`parse_partial_json`  The parser to use. |


