<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/arun -->

Methodv1.2.13 (latest)●Since v1.0Deprecated

# arun

Convenience method for executing chain.

The main difference between this method and `Chain.__call__` is that this
method expects inputs to be passed directly in as positional arguments or
keyword arguments, whereas `Chain.__call__` expects a single input dictionary
with all the inputs


```
arun(
  self,
  *args: Any = (),
  callbacks: Callbacks = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  **kwargs: Any = {}
) -> Any
```

**Example:**

```
# Suppose we have a single-input chain that takes a 'question' string:
await chain.arun("What's the temperature in Boise, Idaho?")
# -> "The temperature in Boise is..."

# Suppose we have a multi-input chain that takes a 'question' string
# and 'context' string:
question = "What's the temperature in Boise, Idaho?"
context = "Weather report for Boise, Idaho on 07/03/23..."
await chain.arun(question=question, context=context)
# -> "The temperature in Boise is..."
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `*args` | `Any` | Default:`()`  If the chain expects a single input, it can be passed in as the sole positional argument. |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to use for this chain run. These will be called in addition to callbacks passed to the chain during construction, but only these runtime callbacks will propagate to calls to other objects. |
| `tags` | `list[str] | None` | Default:`None`  List of string tags to pass to all callbacks. These will be passed in addition to tags passed to the chain during construction, but only these runtime tags will propagate to calls to other objects. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  Optional metadata associated with the chain. |
| `**kwargs` | `Any` | Default:`{}`  If the chain expects multiple inputs, they can be passed in directly as keyword arguments. |


