<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_conversation -->

Methodv1.1.4 (latest)●Since v1.1

# test\_conversation

Test to verify that the model can handle multi-turn conversations.

This should pass for all integrations. Tests the model's ability to process
a sequence of alternating `HumanMessage` and `AIMessage` objects as context for
generating the next response.

Troubleshooting

First, debug
`langchain_tests.integration_tests.chat_models.ChatModelIntegrationTests.test_invoke`
because this test also uses `model.invoke`.

If that test passes but not this one, you should verify that:

1. Your model correctly processes the message history
2. The model maintains appropriate context from previous messages
3. The response is a valid `langchain_core.messages.AIMessage`


```
test_conversation(
    self,
    model: BaseChatModel,
) -> None
```


