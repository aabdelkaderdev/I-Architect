<!-- Source: https://reference.langchain.com/python/langchain-core/messages/block_translators/openai/convert_to_openai_data_block -->

Functionv1.2.21 (latest)●Since v1.0

# convert\_to\_openai\_data\_block

Format standard data content block to format expected by OpenAI.

"Standard data content block" can include old-style LangChain v0 blocks
(URLContentBlock, Base64ContentBlock, IDContentBlock) or new ones.


```
convert_to_openai_data_block(
  block: dict,
  api: Literal['chat/completions', 'responses'] = 'chat/completions'
) -> dict
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `block`\* | `dict` | The content block to convert. |
| `api` | `Literal['chat/completions', 'responses']` | Default:`'chat/completions'`  The OpenAI API being targeted. Either "chat/completions" or "responses". |


