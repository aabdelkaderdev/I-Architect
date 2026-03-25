<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_image_tool_message -->

Methodv1.1.4 (latest)●Since v1.1

# test\_image\_tool\_message

Test that the model can process `ToolMessage` objects with image inputs.

This test should be skipped if the model does not support messages of the
Chat Completions `image_url` format:

```
ToolMessage(
    content=[
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ],
    tool_call_id="1",
    name="random_image",
)
```

In addition, models should support the standard LangChain `ImageContentBlock`
format:

```
ToolMessage(
    content=[
        {
            "type": "image",
            "base64": image_data,
            "mime_type": "image/jpeg",
        },
    ],
    tool_call_id="1",
    name="random_image",
)
```

This test can be skipped by setting the `supports_image_tool_message` property
to `False` (see configuration below).

Configuration

To disable this test, set `supports_image_tool_message` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_image_tool_message(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the model can correctly handle messages
with image content blocks in `ToolMessage` objects, including base64-encoded
images. Otherwise, set the `supports_image_tool_message` property to
`False`.


```
test_image_tool_message(
    self,
    model: BaseChatModel,
) -> None
```


