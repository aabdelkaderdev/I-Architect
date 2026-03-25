<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/bind -->

Methodv1.2.21 (latest)●Since v0.1

# bind

Bind arguments to a `Runnable`, returning a new `Runnable`.

Useful when a `Runnable` in a chain requires an argument that is not
in the output of the previous `Runnable` or included in the user input.


```
bind(
    self,
    **kwargs: Any = {},
) -> Runnable[Input, Output]
```

**Example:**

```
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(model="llama3.1")

# Without bind
chain = model | StrOutputParser()

chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
# Output is 'One two three four five.'

# With bind
chain = model.bind(stop=["three"]) | StrOutputParser()

chain.invoke("Repeat quoted words exactly: 'One two three four five.'")
# Output is 'One two'
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `Any` | Default:`{}`  The arguments to bind to the `Runnable`. |


