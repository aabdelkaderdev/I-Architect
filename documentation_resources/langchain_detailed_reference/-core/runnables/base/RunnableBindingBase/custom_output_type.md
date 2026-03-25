<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBindingBase/custom_output_type -->

Attributev1.2.21 (latest)●Since v0.1

# custom\_output\_type

Override the output type of the underlying `Runnable` with a custom type.

The type can be a Pydantic model, or a type annotation (e.g., `list[str]`).


```
custom_output_type: Any | None = None
```


