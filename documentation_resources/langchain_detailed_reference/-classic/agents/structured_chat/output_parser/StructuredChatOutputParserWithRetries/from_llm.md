<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/output_parser/StructuredChatOutputParserWithRetries/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a StructuredChatOutputParserWithRetries from a language model.


```
from_llm(
  cls,
  llm: BaseLanguageModel | None = None,
  base_parser: StructuredChatOutputParser | None = None
) -> StructuredChatOutputParserWithRetries
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm` | `BaseLanguageModel | None` | Default:`None`  The language model to use. |
| `base_parser` | `StructuredChatOutputParser | None` | Default:`None`  An optional StructuredChatOutputParser to use. |


