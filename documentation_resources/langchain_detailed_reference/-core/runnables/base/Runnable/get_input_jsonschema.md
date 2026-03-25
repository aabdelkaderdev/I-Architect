<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/get_input_jsonschema -->

Methodv1.2.21 (latest)●Since v0.3

# get\_input\_jsonschema

Get a JSON schema that represents the input to the `Runnable`.


```
get_input_jsonschema(
    self,
    config: RunnableConfig | None = None,
) -> dict[str, Any]
```

**Example:**

```
from langchain_core.runnables import RunnableLambda

def add_one(x: int) -> int:
    return x + 1

runnable = RunnableLambda(add_one)

print(runnable.get_input_jsonschema())
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config` | `RunnableConfig | None` | Default:`None`  A config to use when generating the schema. |


