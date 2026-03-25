<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackManager/set_handler -->

Methodv1.2.21 (latest)●Since v0.1

# set\_handler

Set handler as the only handler on the callback manager.


```
set_handler(
  self,
  handler: BaseCallbackHandler,
  inherit: bool = True
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handler`\* | `BaseCallbackHandler` | The handler to set. |
| `inherit` | `bool` | Default:`True`  Whether to inherit the handler. |


