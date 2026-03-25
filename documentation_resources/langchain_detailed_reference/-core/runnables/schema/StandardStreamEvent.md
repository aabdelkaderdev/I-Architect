<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/StandardStreamEvent -->

Classv1.2.21 (latest)●Since v0.2

# StandardStreamEvent

A standard stream event that follows LangChain convention for event data.


```
StandardStreamEvent()
```

## Bases

`BaseStreamEvent`

## Attributes

[attribute

data: EventData

Event data.

The contents of the event data depend on the event type.](/python/langchain-core/runnables/schema/StandardStreamEvent/data)[attribute

name: str

The name of the `Runnable` that generated the event.](/python/langchain-core/runnables/schema/StandardStreamEvent/name)

## Inherited from[BaseStreamEvent](/python/langchain-core/runnables/schema/BaseStreamEvent)

### Attributes

[Aevent: str

—

Event names are of the format: `on_[runnable_type]_(start|stream|end)`.](/python/langchain-core/runnables/schema/BaseStreamEvent/event)[Arun\_id: str

—

An randomly generated ID to keep track of the execution of the given `Runnable`.](/python/langchain-core/runnables/schema/BaseStreamEvent/run_id)[Atags: NotRequired[list[str]]

—

Tags associated with the `Runnable` that generated this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/tags)[Ametadata: NotRequired[dict[str, Any]]

—

Metadata associated with the `Runnable` that generated this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/metadata)[Aparent\_ids: Sequence[str]

—

A list of the parent IDs associated with this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/parent_ids)


