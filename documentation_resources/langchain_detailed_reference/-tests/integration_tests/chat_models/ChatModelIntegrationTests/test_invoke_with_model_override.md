<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_invoke_with_model_override -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke\_with\_model\_override

Test that model name can be overridden at invoke time via kwargs.

This enables dynamic model selection without creating new instances,
which is useful for fallback strategies, A/B testing, or cost optimization.

Test is skipped if `supports_model_override` is `False`.

Troubleshooting

If this test fails, ensure that your `_generate` method passes
`**kwargs` through to the API request payload in a way that allows
the `model` parameter to be overridden.

For example:

```
def _get_request_payload(self, ..., **kwargs) -> dict:
    return {
        "model": self.model,
        ...
        **kwargs,  # kwargs should come last to allow overrides
    }
```


```
test_invoke_with_model_override(
    self,
    model: BaseChatModel,
) -> None
```


