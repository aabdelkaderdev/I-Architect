<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLike -->

Typev1.2.21 (latest)●Since v0.1

# RunnableLike


```
RunnableLike = Runnable[Input, Output] | Callable[[Input], Output] | Callable[[Input], Awaitable[Output]] | Callable[[Iterator[Input]], Iterator[Output]] | Callable[[AsyncIterator[Input]], AsyncIterator[Output]] | _RunnableCallableSync[Input, Output] | _RunnableCallableAsync[Input, Output] | _RunnableCallableIterator[Input, Output] | _RunnableCallableAsyncIterator[Input, Output] | Mapping[str, Any]
```


