<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/prompt/PromptTemplate/from_file -->

Methodv1.2.21 (latest)●Since v0.1

# from\_file

Load a prompt from a file.


```
from_file(
  cls,
  template_file: str | Path,
  encoding: str | None = None,
  **kwargs: Any = {}
) -> PromptTemplate
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template_file`\* | `str | Path` | The path to the file containing the prompt template. |
| `encoding` | `str | None` | Default:`None`  The encoding system for opening the template file.  If not provided, will use the OS default. |


