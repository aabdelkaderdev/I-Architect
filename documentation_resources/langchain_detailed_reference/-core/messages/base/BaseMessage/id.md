<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage/id -->

Attributev1.2.21 (latest)●Since v0.1

# id

An optional unique identifier for the message.

This should ideally be provided by the provider/model which created the message.


```
id: str | None = Field(default=None, coerce_numbers_to_str=True)
```


