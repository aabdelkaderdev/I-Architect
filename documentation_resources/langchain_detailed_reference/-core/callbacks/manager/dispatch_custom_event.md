<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/dispatch_custom_event -->

Functionv1.2.21 (latest)●Since v0.2

# dispatch\_custom\_event

Dispatch an adhoc event.


```
dispatch_custom_event(
  name: str,
  data: Any,
  *,
  config: RunnableConfig | None = None
) -> None
```

**Example:**

```
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.callbacks import dispatch_custom_event
from langchain_core.runnable import RunnableLambda

class CustomCallbackManager(BaseCallbackHandler):
    def on_custom_event(
        self,
        name: str,
        data: Any,
        *,
        run_id: UUID,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        print(f"Received custom event: {name} with data: {data}")

def foo(inputs):
    dispatch_custom_event("my_event", {"bar": "buzz})
    return inputs

foo_ = RunnableLambda(foo)
foo_.invoke({"a": "1"}, {"callbacks": [CustomCallbackManager()]})
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | The name of the adhoc event. |
| `data`\* | `Any` | The data for the adhoc event.  Free form data. Ideally should be JSON serializable to avoid serialization issues downstream, but this is not enforced. |
| `config` | `RunnableConfig | None` | Default:`None`  Optional config object.  Mirrors the async API but not strictly needed. |


