<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/BaseStreamEvent/tags -->

Attributev1.2.21 (latest)●Since v0.2

# tags

Tags associated with the `Runnable` that generated this event.

Tags are always inherited from parent `Runnable` objects.

Tags can either be bound to a `Runnable` using `.with_config({"tags": ["hello"]})`
or passed at run time using `.astream_events(..., {"tags": ["hello"]})`.


```
tags: NotRequired[list[str]]
```


