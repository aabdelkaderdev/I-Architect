<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/fallbacks/RunnableWithFallbacks/exceptions_to_handle -->

Attributev1.2.21 (latest)●Since v0.1

# exceptions\_to\_handle

The exceptions on which fallbacks should be tried.

Any exception that is not a subclass of these exceptions will be raised immediately.


```
exceptions_to_handle: tuple[type[BaseException], ...] = (Exception,)
```


