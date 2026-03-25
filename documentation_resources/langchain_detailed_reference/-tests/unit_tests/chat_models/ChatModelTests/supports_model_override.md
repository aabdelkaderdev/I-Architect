<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supports_model_override -->

Attributev1.1.4 (latest)●Since v1.1

# supports\_model\_override

Whether the model supports overriding the model name at runtime.

Defaults to `True`.

If `True`, the model accepts a `model` kwarg in `invoke()`, `stream()`,
etc. that overrides the model specified at initialization.

This enables dynamic model selection without creating new instances.


```
supports_model_override: bool
```


