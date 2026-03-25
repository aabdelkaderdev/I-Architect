<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_usage_metadata_streaming -->

Methodv1.1.4 (latest)●Since v1.1

# test\_usage\_metadata\_streaming

Test usage metadata in streaming mode.

Test to verify that the model returns correct usage metadata in streaming mode.

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

If this test fails, first verify that your model yields
`langchain_core.messages.ai.UsageMetadata` dicts
attached to the returned `AIMessage` object in `_stream`
that sum up to the total usage metadata.

Note that `input_tokens` should only be included on one of the chunks
(typically the first or the last chunk), and the rest should have `0` or
`None` to avoid counting input tokens multiple times.

`output_tokens` typically count the number of tokens in each chunk, not
the sum. This test will pass as long as the sum of `output_tokens` across
all chunks is not `0`.

```
yield ChatResult(
    generations=[
        ChatGeneration(
            message=AIMessage(
                content="Output text",
                usage_metadata={
                    "input_tokens": (
                        num_input_tokens if is_first_chunk else 0
                    ),
                    "output_tokens": 11,
                    "total_tokens": (
                        11 + num_input_tokens if is_first_chunk else 11
                    ),
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

Check also that the aggregated response includes a `model_name` key
in its `usage_metadata`.


```
test_usage_metadata_streaming(
    self,
    model: BaseChatModel,
) -> None
```


