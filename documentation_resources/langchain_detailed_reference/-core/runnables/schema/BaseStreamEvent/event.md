<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/BaseStreamEvent/event -->

Attributev1.2.21 (latest)●Since v0.2

# event

Event names are of the format: `on_[runnable_type]_(start|stream|end)`.

Runnable types are one of:

- **llm** - used by non chat models
- **chat\_model** - used by chat models
- **prompt** -- e.g., `ChatPromptTemplate`
- **tool** -- from tools defined via `@tool` decorator or inheriting
  from `Tool`/`BaseTool`
- **chain** - most `Runnable` objects are of this type

Further, the events are categorized as one of:

- **start** - when the `Runnable` starts
- **stream** - when the `Runnable` is streaming
- \**end* - when the `Runnable` ends

start, stream and end are associated with slightly different `data` payload.

Please see the documentation for `EventData` for more details.


```
event: str
```


