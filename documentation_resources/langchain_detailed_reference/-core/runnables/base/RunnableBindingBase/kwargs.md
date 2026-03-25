<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableBindingBase/kwargs -->

Attributev1.2.21 (latest)●Since v0.1

# kwargs

kwargs to pass to the underlying `Runnable` when running.

For example, when the `Runnable` binding is invoked the underlying
`Runnable` will be invoked with the same input but with these additional
kwargs.


```
kwargs: Mapping[str, Any] = Field(default_factory=dict)
```


