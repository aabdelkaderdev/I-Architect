<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/merge_content -->

Functionv1.2.21 (latest)●Since v0.1

# merge\_content

Merge multiple message contents.


```
merge_content(
  first_content: str | list[str | dict],
  *contents: str | list[str | dict] = ()
) -> str | list[str | dict]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `first_content`\* | `str | list[str | dict]` | The first `content`. Can be a string or a list. |
| `contents` | `str | list[str | dict]` | Default:`()`  The other `content`s. Can be a string or a list. |


