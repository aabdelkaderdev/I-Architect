<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/_utils/is_openai_data_block -->

Functionv1.2.21 (latest)●Since v1.0

# is\_openai\_data\_block

Check whether a block contains multimodal data in OpenAI Chat Completions format.

Supports both data and ID-style blocks (e.g. `'file_data'` and `'file_id'`)

If additional keys are present, they are ignored / will not affect outcome as long
as the required keys are present and valid.


```
is_openai_data_block(
  block: dict,
  filter_: Literal['image', 'audio', 'file'] | None = None
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `block`\* | `dict` | The content block to check. |
| `filter_` | `Literal['image', 'audio', 'file'] | None` | Default:`None`  If provided, only return True for blocks matching this specific type.   - "image": Only match image\_url blocks - "audio": Only match input\_audio blocks - "file": Only match file blocks   If `None`, match any valid OpenAI data block type. Note that this means that   if the block has a valid OpenAI data type but the filter\_ is set to a   different type, this function will return False. |


