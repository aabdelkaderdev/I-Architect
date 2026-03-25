<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_pdf_inputs -->

Methodv1.1.4 (latest)●Since v1.1

# test\_pdf\_inputs

Test that the model can process PDF inputs.

This test should be skipped (see configuration below) if the model does not
support PDF inputs. These will take the shape of the LangChain
`FileContentBlock`:

```
{
    "type": "image",
    "base64": "<base64 image data>",
    "mime_type": "application/pdf",
}
```

Furthermore, for backward-compatibility, we must also support OpenAI chat
completions file content blocks:

```
(
    {
        "type": "file",
        "file": {
            "filename": "test_file.pdf",
            "file_data": f"data:application/pdf;base64,{pdf_data}",
        },
    },
)
```

Configuration

To disable this test, set `supports_pdf_inputs` to `False` in your
test class:

```
class TestMyChatModelIntegration(ChatModelIntegrationTests):
    @property
    def supports_pdf_inputs(self) -> bool:
        return False
```

Troubleshooting

If this test fails, check that the model can correctly handle messages
with pdf content blocks, including base64-encoded files. Otherwise, set
the `supports_pdf_inputs` property to `False`.


```
test_pdf_inputs(
    self,
    model: BaseChatModel,
) -> None
```


