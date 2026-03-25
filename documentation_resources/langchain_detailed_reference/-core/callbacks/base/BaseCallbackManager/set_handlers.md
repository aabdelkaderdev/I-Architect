<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackManager/set_handlers -->

Methodv1.2.21 (latest)●Since v0.1

# set\_handlers

Set handlers as the only handlers on the callback manager.


```
set_handlers(
  self,
  handlers: list[BaseCallbackHandler],
  inherit: bool = True
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handlers`\* | `list[BaseCallbackHandler]` | The handlers to set. |
| `inherit` | `bool` | Default:`True`  Whether to inherit the handlers. |


