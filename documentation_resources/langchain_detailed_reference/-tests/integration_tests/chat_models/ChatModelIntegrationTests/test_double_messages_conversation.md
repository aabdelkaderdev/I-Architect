<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_double_messages_conversation -->

Methodv1.1.4 (latest)●Since v1.1

# test\_double\_messages\_conversation

Test to verify that the model can handle double-message conversations.

This should pass for all integrations. Tests the model's ability to process
a sequence of double-system, double-human, and double-ai messages as context
for generating the next response.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_invoke`
because this test also uses `model.invoke`.

Second, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_conversation`
because this test is the "basic case" without double messages.

If that test passes those but not this one, you should verify that:

1. Your model API can handle double messages, or the integration should
   merge messages before sending them to the API.
2. The response is a valid `langchain_core.messages.AIMessage`


```
test_double_messages_conversation(
    self,
    model: BaseChatModel,
) -> None
```


