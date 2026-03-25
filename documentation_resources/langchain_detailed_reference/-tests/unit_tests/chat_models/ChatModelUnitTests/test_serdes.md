<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/chat_models/ChatModelUnitTests/test_serdes -->

Methodv1.1.4 (latest)●Since v1.1

# test\_serdes

Test serialization and deserialization of the model.

Test is skipped if the `is_lc_serializable` property on the chat model class
is not overwritten to return `True`.

Troubleshooting

If this test fails, check that the `init_from_env_params` property is
correctly set on the test class.


```
test_serdes(
  self,
  model: BaseChatModel,
  snapshot: SnapshotAssertion
) -> None
```


