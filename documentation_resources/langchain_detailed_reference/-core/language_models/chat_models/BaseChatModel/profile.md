<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/profile -->

Attributev1.2.21 (latest)●Since v1.0

# profile

Profile detailing model capabilities.

Beta feature

This is a beta feature. The format of model profiles is subject to change.

If not specified, automatically loaded from the provider package on initialization
if data is available.

Example profile data includes context window sizes, supported modalities, or support
for tool calling, structured output, and other features.


```
profile: ModelProfile | None = Field(default=None, exclude=True)
```


