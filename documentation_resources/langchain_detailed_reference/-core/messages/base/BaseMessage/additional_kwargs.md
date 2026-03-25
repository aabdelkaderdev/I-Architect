<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage/additional_kwargs -->

Attributev1.2.21 (latest)●Since v0.1

# additional\_kwargs

Reserved for additional payload data associated with the message.

For example, for a message from an AI, this could include tool calls as
encoded by the model provider.


```
additional_kwargs: dict = Field(default_factory=dict)
```


