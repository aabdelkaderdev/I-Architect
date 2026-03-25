<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/file/FileCallbackHandler/on_text -->

Methodv1.2.21 (latest)●Since v0.1

# on\_text

Handle text output.


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
| `text`\* | `str` | The text to write. |
| `color` | `str | None` | Default:`None`  Color override for this specific output.  If `None`, uses `self.color`. |
| `end` | `str` | Default:`''`  String appended after the text. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |


