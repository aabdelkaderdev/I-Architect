<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives -->

Methodv1.2.21 (latest)●Since v0.1

# configurable\_alternatives

Configure alternatives for `Runnable` objects that can be set at runtime.


```
configurable_alternatives(
  self,
  which: ConfigurableField,
  *,
  default_key: str = 'default',
  prefix_keys: bool = False,
  **kwargs: Runnable[Input, Output] | Callable[[], Runnable[Input, Output]] = {}
) -> RunnableSerializable[Input, Output]
```

```
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables.utils import ConfigurableField
from langchain_openai import ChatOpenAI

model = ChatAnthropic(
    model_name="claude-sonnet-4-5-20250929"
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="anthropic",
    openai=ChatOpenAI(),
)

# uses the default model ChatAnthropic
print(model.invoke("which organization created you?").content)

# uses ChatOpenAI
print(
    model.with_config(configurable={"llm": "openai"})
    .invoke("which organization created you?")
    .content
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `which`\* | `ConfigurableField` | The `ConfigurableField` instance that will be used to select the alternative. |
| `default_key` | `str` | Default:`'default'`  The default key to use if no alternative is selected. |
| `prefix_keys` | `bool` | Default:`False`  Whether to prefix the keys with the `ConfigurableField` id. |
| `**kwargs` | `Runnable[Input, Output] | Callable[[], Runnable[Input, Output]]` | Default:`{}`  A dictionary of keys to `Runnable` instances or callables that return `Runnable` instances. |


