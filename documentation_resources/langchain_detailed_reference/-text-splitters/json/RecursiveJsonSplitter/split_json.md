<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/json/RecursiveJsonSplitter/split_json -->

Methodv1.1.1 (latest)●Since v0.0

# split\_json

Splits JSON into a list of JSON chunks.


```
split_json(
  self,
  json_data: dict[str, Any],
  convert_lists: bool = False
) -> list[dict[str, Any]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `json_data`\* | `dict[str, Any]` | The JSON data to be split. |
| `convert_lists` | `bool` | Default:`False`  Whether to convert lists in the JSON to dictionaries before splitting. |


