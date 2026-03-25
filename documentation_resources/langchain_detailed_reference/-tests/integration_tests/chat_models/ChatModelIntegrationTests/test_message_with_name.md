<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_message_with_name -->

Methodv1.1.4 (latest)●Since v1.1

# test\_message\_with\_name

Test that `HumanMessage` with values for the `name` field can be handled.

These messages may take the form:

```
HumanMessage("hello", name="example_user")
```

If possible, the `name` field should be parsed and passed appropriately
to the model. Otherwise, it should be ignored.

Troubleshooting

If this test fails, check that the `name` field on `HumanMessage`
objects is either ignored or passed to the model appropriately.


```
test_message_with_name(
    self,
    model: BaseChatModel,
) -> None
```


