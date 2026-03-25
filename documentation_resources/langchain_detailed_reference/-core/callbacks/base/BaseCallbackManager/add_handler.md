<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackManager/add_handler -->

Methodv1.2.21 (latest)●Since v0.1

# add\_handler

Add a handler to the callback manager.


```
add_handler(
  self,
  handler: BaseCallbackHandler,
  inherit: bool = True
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handler`\* | `BaseCallbackHandler` | The handler to add. |
| `inherit` | `bool` | Default:`True`  Whether to inherit the handler. |


