<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelTests/supported_usage_metadata_details -->

Attributev1.1.4 (latest)●Since v1.1

# supported\_usage\_metadata\_details

Supported usage metadata details.

What usage metadata details are emitted in invoke and stream. Only needs to be
overridden if these details are returned by the model.


```
supported_usage_metadata_details: dict[Literal['invoke', 'stream'], list[Literal['audio_input', 'audio_output', 'reasoning_output', 'cache_read_input', 'cache_creation_input']]]
```


