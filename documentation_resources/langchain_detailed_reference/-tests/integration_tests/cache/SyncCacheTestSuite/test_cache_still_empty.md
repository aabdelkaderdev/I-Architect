<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/cache/SyncCacheTestSuite/test_cache_still_empty -->

Methodv1.1.4 (latest)●Since v1.1

# test\_cache\_still\_empty

Test that the cache is still empty.

This test should follow a test that updates the cache.

This just verifies that the fixture is set up properly to be empty after each
test.


```
test_cache_still_empty(
    self,
    cache: BaseCache,
) -> None
```


