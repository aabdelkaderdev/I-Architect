<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/html/HTMLHeaderTextSplitter/split_text_from_url -->

Methodv1.1.1 (latest)●Since v0.0

# split\_text\_from\_url

Fetch text content from a URL and split it into documents.


```
split_text_from_url(
  self,
  url: str,
  timeout: int = 10,
  **kwargs: Any = {}
) -> list[Document]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url`\* | `str` | The URL to fetch content from. |
| `timeout` | `int` | Default:`10`  Timeout for the request. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments for the request. |


