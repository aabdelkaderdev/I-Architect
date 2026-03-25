<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/context/collect_runs -->

Functionv1.2.21 (latest)●Since v0.1

# collect\_runs

Collect all run traces in context.


```
collect_runs() -> Generator[RunCollectorCallbackHandler, None, None]
```

**Example:**

> > > with collect\_runs() as runs\_cb:
> > > chain.invoke("foo")
> > > run\_id = runs\_cb.traced\_runs[0].id


