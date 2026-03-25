<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/context/tracing_v2_enabled -->

Functionv1.2.21 (latest)●Since v0.1

# tracing\_v2\_enabled

Instruct LangChain to log all runs in context to LangSmith.


```
tracing_v2_enabled(
  project_name: str | None = None,
  *,
  example_id: str | UUID | None = None,
  tags: list[str] | None = None,
  client: LangSmithClient | None = None
) -> Generator[LangChainTracer, None, None]
```

**Example:**

> > > with tracing\_v2\_enabled():
> > > ... # LangChain code will automatically be traced

You can use this to fetch the LangSmith run URL:

> > > with tracing\_v2\_enabled() as cb:
> > > ... chain.invoke("foo")
> > > ... run\_url = cb.get\_run\_url()

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `project_name` | `str | None` | Default:`None`  The name of the project.  Defaults to `'default'`. |
| `example_id` | `str | UUID | None` | Default:`None`  The ID of the example. |
| `tags` | `list[str] | None` | Default:`None`  The tags to add to the run. |
| `client` | `LangSmithClient | None` | Default:`None`  The client of the langsmith. |


