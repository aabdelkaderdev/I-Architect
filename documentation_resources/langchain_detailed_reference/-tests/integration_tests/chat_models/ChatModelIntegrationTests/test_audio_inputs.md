<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_audio_inputs -->

Methodv1.1.4 (latest)●Since v1.1

# test\_audio\_inputs

Test that the model can process audio inputs.

This test should be skipped (see configuration below) if the model does not
support audio inputs. These will take the shape of the LangChain
`AudioContentBlock`:

```
{
    "type": "audio",
    "base64": "<base64 audio data>",
    "mime_type": "audio/wav",  # or appropriate MIME type
}
```

Furthermore, for backward-compatibility, we must also support OpenAI chat
completions audio content blocks:

```
{
    "type": "input_audio",
    "input_audio": {
        "data": "<base64 audio data>",
        "format": "wav",  # or appropriate format
    },
}
```

Note: this test downloads audio data from wikimedia.org. You may need to set
the `LANGCHAIN_TESTS_USER_AGENT` environment variable to identify these
requests, e.g.,

```
export LANGCHAIN_TESTS_USER_AGENT="CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0"
```

Refer to the [Wikimedia Foundation User-Agent Policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy).

Configuration

To disable this test, set `supports_audio_inputs` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_audio_inputs(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the model can correctly handle messages
with audio content blocks, specifically base64-encoded files. Otherwise,
set the `supports_audio_inputs` property to `False`.


```
test_audio_inputs(
    self,
    model: BaseChatModel,
) -> None
```


