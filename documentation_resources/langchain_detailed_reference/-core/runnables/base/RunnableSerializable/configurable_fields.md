<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields -->

Methodv1.2.21 (latest)●Since v0.1

# configurable\_fields

Configure particular `Runnable` fields at runtime.


```
configurable_fields(
  self,
  **kwargs: AnyConfigurableField = {}
) -> RunnableSerializable[Input, Output]
```

```
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

model = ChatOpenAI(max_tokens=20).configurable_fields(
    max_tokens=ConfigurableField(
        id="output_token_number",
        name="Max tokens in the output",
        description="The maximum number of tokens in the output",
    )
)

# max_tokens = 20
print(
    "max_tokens_20: ", model.invoke("tell me something about chess").content
)

# max_tokens = 200
print(
    "max_tokens_200: ",
    model.with_config(configurable={"output_token_number": 200})
    .invoke("tell me something about chess")
    .content,
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `AnyConfigurableField` | Default:`{}`  A dictionary of `ConfigurableField` instances to configure. |


