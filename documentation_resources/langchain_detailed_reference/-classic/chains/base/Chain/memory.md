<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/memory -->

Attributev1.2.13 (latest)●Since v1.0

# memory

Optional memory object.
Memory is a class that gets called at the start
and at the end of every chain. At the start, memory loads variables and passes
them along in the chain. At the end, it saves any returned variables.
There are many different types of memory - please see memory docs
for the full catalog.


```
memory: BaseMemory | None = None
```


