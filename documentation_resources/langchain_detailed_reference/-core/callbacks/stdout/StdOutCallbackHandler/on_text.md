<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/stdout/StdOutCallbackHandler/on_text -->

Methodv1.2.21 (latest)●Since v0.1

# on\_text

Run when the agent ends.


```
on_text(
  self,
  text: str,
  color: str | None = None,
  end: str = '',
  **kwargs: Any = {}
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text to print. |
| `color` | `str | None` | Default:`None`  The color to use for the text. |
| `end` | `str` | Default:`''`  The end character to use. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


