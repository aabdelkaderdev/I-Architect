<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter/from_language -->

Methodv1.1.1 (latest)●Since v0.0

# from\_language


```
from_language(
  cls,
  language: Language,
  **kwargs: Any = {}
) -> RecursiveCharacterTextSplitter
```



## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `language`\* | `Language` | The language to configure the text splitter for. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to customize the splitter. |

Return an instance of this class based on a specific language.

This method initializes the text splitter with language-specific separators.