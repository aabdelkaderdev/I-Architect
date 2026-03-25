<!-- Source: https://reference.langchain.com/python/langchain-core/messages/content/is_data_content_block -->

Functionv1.2.21 (latest)●Since v1.0

# is\_data\_content\_block

Check if the provided content block is a data content block.

Returns True for both v0 (old-style) and v1 (new-style) multimodal data blocks.


```
is_data_content_block(
    block: dict,
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `block`\* | `dict` | The content block to check. |


