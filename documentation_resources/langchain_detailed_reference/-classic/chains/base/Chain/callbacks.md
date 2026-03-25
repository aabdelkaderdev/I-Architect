<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/callbacks -->

Attributev1.2.13 (latest)●Since v1.0

# callbacks

Optional list of callback handlers (or callback manager).
Callback handlers are called throughout the lifecycle of a call to a chain,
starting with on\_chain\_start, ending with on\_chain\_end or on\_chain\_error.
Each custom chain can optionally call additional callback methods, see Callback docs
for full details.


```
callbacks: Callbacks = Field(default=None, exclude=True)
```


