<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm/LLMChain/apredict -->

Methodv1.2.13 (latest)●Since v1.0

# apredict

Format prompt with kwargs and pass to LLM.


```
apredict(
  self,
  callbacks: Callbacks = None,
  **kwargs: Any = {}
) -> str
```

**Example:**

```
completion = llm.predict(adjective="funny")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `callbacks` | `Callbacks` | Default:`None`  Callbacks to pass to LLMChain |
| `**kwargs` | `Any` | Default:`{}`  Keys to pass to prompt template. |


