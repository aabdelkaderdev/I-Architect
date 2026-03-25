<!-- Source: https://reference.langchain.com/python/langchain-core/utils/json/parse_and_check_json_markdown -->

Functionv1.2.21 (latest)●Since v0.1

# parse\_and\_check\_json\_markdown

Parse and check a JSON string from a Markdown string.

Checks that it contains the expected keys.


```
parse_and_check_json_markdown(
    text: str,
    expected_keys: list[str],
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The Markdown string. |
| `expected_keys`\* | `list[str]` | The expected keys in the JSON string. |


