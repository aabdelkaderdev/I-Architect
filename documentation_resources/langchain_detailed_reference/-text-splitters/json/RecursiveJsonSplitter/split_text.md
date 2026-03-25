<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/json/RecursiveJsonSplitter/split_text -->

Methodv1.1.1 (latest)●Since v0.0

# split\_text

Splits JSON into a list of JSON formatted strings.


```
split_text(
  self,
  json_data: dict[str, Any],
  convert_lists: bool = False,
  ensure_ascii: bool = True
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `json_data`\* | `dict[str, Any]` | The JSON data to be split. |
| `convert_lists` | `bool` | Default:`False`  Whether to convert lists in the JSON to dictionaries before splitting. |
| `ensure_ascii` | `bool` | Default:`True`  Whether to ensure ASCII encoding in the JSON strings. |


