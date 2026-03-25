<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/get_output_jsonschema -->

Methodv1.2.21 (latest)●Since v0.3

# get\_output\_jsonschema

Get a JSON schema that represents the output of the `Runnable`.


```
get_output_jsonschema(
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

print(runnable.get_output_jsonschema())
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `config` | `RunnableConfig | None` | Default:`None`  A config to use when generating the schema. |


