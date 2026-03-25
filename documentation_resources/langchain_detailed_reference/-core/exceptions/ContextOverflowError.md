<!-- Source: https://reference.langchain.com/python/langchain-core/exceptions/ContextOverflowError -->

Classv1.2.21 (latest)●Since v1.2

# ContextOverflowError

Exception raised when input exceeds the model's context limit.

This exception is raised by chat models when the input tokens exceed
the maximum context window supported by the model.


```
ContextOverflowError()
```

## Bases

`LangChainException`


