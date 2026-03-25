<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/BaseStreamEvent/run_id -->

Attributev1.2.21 (latest)●Since v0.2

# run\_id

An randomly generated ID to keep track of the execution of the given `Runnable`.

Each child `Runnable` that gets invoked as part of the execution of a parent
`Runnable` is assigned its own unique ID.


```
run_id: str
```


