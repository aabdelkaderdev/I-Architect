<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_pdf_tool_message -->

Methodv1.1.4 (latest)●Since v1.1

# test\_pdf\_tool\_message

Test that the model can process `ToolMessage` objects with PDF inputs.

This test should be skipped if the model does not support messages of the
LangChain `FileContentBlock` format:

```
ToolMessage(
    content=[
        {
            "type": "file",
            "base64": pdf_data,
            "mime_type": "application/pdf",
        },
    ],
    tool_call_id="1",
    name="random_pdf",
)
```

This test can be skipped by setting the `supports_pdf_tool_message` property
to `False` (see configuration below).

Configuration

To disable this test, set `supports_pdf_tool_message` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_pdf_tool_message(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the model can correctly handle messages
with PDF content blocks in `ToolMessage` objects, specifically
base64-encoded PDFs. Otherwise, set the `supports_pdf_tool_message` property
to `False`.


```
test_pdf_tool_message(
    self,
    model: BaseChatModel,
) -> None
```


