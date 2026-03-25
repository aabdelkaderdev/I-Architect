<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_invoke_with_k_kwarg -->

Methodv1.1.4 (latest)●Since v1.1

# test\_invoke\_with\_k\_kwarg

Test the number of results parameter in `invoke`.

Test that the invoke method accepts a parameter representing
the number of documents to return.

By default, the parameter is named, but it can be overridden by
setting the `num_results_arg_name` property.

Note

If the retriever doesn't support configuring the number of results returned
via the invoke method, this test can be skipped using a pytest `xfail` on
the test class:

```
@pytest.mark.xfail(
    reason="This retriever doesn't support setting "
    "the number of results in the invoke method."
)
def test_invoke_with_k_kwarg(self) -> None:
    raise NotImplementedError
```

Troubleshooting

If this test fails, the retriever's invoke method does not accept a number
of results parameter, or the retriever does not return the correct number
of documents (`k` of the one set in `num_results_arg_name`) when it is
set.

For example, a retriever like...

```
MyRetriever().invoke("query", k=3)
```

...should return 3 documents when invoked with a query.


```
test_invoke_with_k_kwarg(
    self,
    retriever: BaseRetriever,
) -> None
```


