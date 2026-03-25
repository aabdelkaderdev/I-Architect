<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_usage_metadata -->

Methodv1.1.4 (latest)●Since v1.1

# test\_usage\_metadata

Test to verify that the model returns correct usage metadata.

This test is optional and should be skipped if the model does not return
usage metadata (see configuration below).

Behavior changed in `langchain-tests` 0.3.17

Additionally check for the presence of `model_name` in the response
metadata, which is needed for usage tracking in callback handlers.

Configuration

By default, this test is run.

To disable this feature, set `returns_usage_metadata` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def returns_usage_metadata(self) -> bool:
        return False
```

This test can also check the format of specific kinds of usage metadata
based on the `supported_usage_metadata_details` property.

This property should be configured as follows with the types of tokens that
the model supports tracking:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supported_usage_metadata_details(self) -> dict:
        return {
            "invoke": [
                "audio_input",
                "audio_output",
                "reasoning_output",
                "cache_read_input",
                "cache_creation_input",
            ],
            "stream": [
                "audio_input",
                "audio_output",
                "reasoning_output",
                "cache_read_input",
                "cache_creation_input",
            ],
        }
```

Troubleshooting

If this test fails, first verify that your model returns
`langchain_core.messages.ai.UsageMetadata` dicts
attached to the returned `AIMessage` object in `_generate`:

```
return ChatResult(
    generations=[
        ChatGeneration(
            message=AIMessage(
                content="Output text",
                usage_metadata={
                    "input_tokens": 350,
                    "output_tokens": 240,
                    "total_tokens": 590,
                    "input_token_details": {
                        "audio": 10,
                        "cache_creation": 200,
                        "cache_read": 100,
                    },
                    "output_token_details": {
                        "audio": 10,
                        "reasoning": 200,
                    },
                },
            )
        )
    ]
)
```

Check also that the response includes a `model_name` key in its
`usage_metadata`.


```
test_usage_metadata(
    self,
    model: BaseChatModel,
) -> None
```


