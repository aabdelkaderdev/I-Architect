<!-- Source: https://reference.langchain.com/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests -->

Classv1.1.4 (latest)●Since v1.1

# RetrieversIntegrationTests


```
RetrieversIntegrationTests()
```

## Bases

`BaseStandardTests`

## Attributes

## Methods

## Inherited from[BaseStandardTests](/python/langchain-tests/base/BaseStandardTests)

### Methods

[Mtest\_no\_overrides\_DO\_NOT\_OVERRIDE

—

Test that no standard tests are overridden.](/python/langchain-tests/base/BaseStandardTests/test_no_overrides_DO_NOT_OVERRIDE)



[attribute

retriever\_constructor: type[BaseRetriever]

A `BaseRetriever` subclass to be tested.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/retriever_constructor)

[attribute

retriever\_constructor\_params: dict[str, Any]

Returns a dictionary of parameters to pass to the retriever constructor.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/retriever_constructor_params)

[attribute

retriever\_query\_example: str

Returns a str representing the `query` of an example retriever call.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/retriever_query_example)

[attribute

num\_results\_arg\_name: str

Returns the name of the parameter for the number of results returned.

Usually something like `k` or `top_k`.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/num_results_arg_name)

[method

retriever

Return retriever fixture.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/retriever)

[method

test\_k\_constructor\_param

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

...should return 3 documents when invoked with a query.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_k_constructor_param)

[method

test\_invoke\_with\_k\_kwarg

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

...should return 3 documents when invoked with a query.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_invoke_with_k_kwarg)

[method

test\_invoke\_returns\_documents

Test invoke returns documents.

If invoked with the example params, the retriever should return a list of
Documents.

Troubleshooting

If this test fails, the retriever's invoke method does not return a list of
`Document` objects. Please confirm that your
`_get_relevant_documents` method returns a list of `Document` objects.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_invoke_returns_documents)

[method

test\_ainvoke\_returns\_documents

Test ainvoke returns documents.

If `ainvoke`'d with the example params, the retriever should return a list of
`Document` objects.

See `test_invoke_returns_documents` for more information on
troubleshooting.](/python/langchain-tests/integration_tests/retrievers/RetrieversIntegrationTests/test_ainvoke_returns_documents)

Base class for retrievers integration tests.