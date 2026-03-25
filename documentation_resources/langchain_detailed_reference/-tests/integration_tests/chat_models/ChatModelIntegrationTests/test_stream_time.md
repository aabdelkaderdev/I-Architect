<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/chat_models/ChatModelIntegrationTests/test_stream_time -->

Methodv1.1.4 (latest)●Since v1.1

# test\_stream\_time

Test that streaming does not introduce undue overhead.

See `enable_vcr_tests` dropdown `above <ChatModelIntegrationTests>`
for more information.

Configuration

This test can be enabled or disabled using the `enable_vcr_tests`
property. For example, to disable the test, set this property to `False`:

```
@property
def enable_vcr_tests(self) -> bool:
    return False
```

Warning

VCR will by default record authentication headers and other sensitive
information in cassettes. See `enable_vcr_tests` dropdown
`above <ChatModelIntegrationTests>` for how to configure what
information is recorded in cassettes.


```
test_stream_time(
  self,
  model: BaseChatModel,
  benchmark: BenchmarkFixture,
  vcr: Cassette
) -> None
```


