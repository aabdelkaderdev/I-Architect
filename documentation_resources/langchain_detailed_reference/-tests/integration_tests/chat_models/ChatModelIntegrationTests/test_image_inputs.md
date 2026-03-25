<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_image_inputs -->

Methodv1.1.4 (latest)●Since v1.1

# test\_image\_inputs

Test that the model can process image inputs.

This test should be skipped (see configuration below) if the model does not
support image inputs. These will take the shape of the LangChain
`ImageContentBlock`:

```
{
    "type": "image",
    "base64": "<base64 image data>",
    "mime_type": "image/jpeg",  # or appropriate MIME type
}
```

For backward-compatibility, we must also support OpenAI chat completions
image content blocks containing base64-encoded images:

```
[
    {"type": "text", "text": "describe the weather in this image"},
    {
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
    },
]
```

See docs for [Multimodality](https://docs.langchain.com/oss/python/langchain/models#multimodal).

If the property `supports_image_urls` is set to `True`, the test will also
check that we can process content blocks of the form:

```
{
    "type": "image",
    "url": "<url>",
}
```

Configuration

To disable this test, set `supports_image_inputs` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_image_inputs(self) -> bool:
        return False

    # Can also explicitly disable testing image URLs:
    @property
    def supports_image_urls(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the model can correctly handle messages
with image content blocks, including base64-encoded images. Otherwise, set
the `supports_image_inputs` property to `False`.


```
test_image_inputs(
    self,
    model: BaseChatModel,
) -> None
```


