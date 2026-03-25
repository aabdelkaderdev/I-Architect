<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_k_constructor_param -->

Methodv1.1.4 (latest)●Since v1.1

# test\_k\_constructor\_param

Test the number of results constructor parameter.

Test that the retriever constructor accepts a parameter representing
the number of documents to return.

By default, the parameter tested is named `k`, but it can be overridden by
setting the `num_results_arg_name` property.

Note

If the retriever doesn't support configuring the number of results returned
via the constructor, this test can be skipped using a pytest `xfail` on
the test class:

```
@pytest.mark.xfail(
    reason="This retriever doesn't support setting "
    "the number of results via the constructor."
)
def test_k_constructor_param(self) -> None:
    raise NotImplementedError
```

Troubleshooting

If this test fails, the retriever constructor does not accept a number
of results parameter, or the retriever does not return the correct number
of documents ( of the one set in `num_results_arg_name`) when it is
set.

For example, a retriever like...

```
MyRetriever(k=3).invoke("query")
```

...should return 3 documents when invoked with a query.


```
test_k_constructor_param(
    self,
) -> None
```


