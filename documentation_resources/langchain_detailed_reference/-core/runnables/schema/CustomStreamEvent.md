<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/schema/CustomStreamEvent -->

Classv1.2.21 (latest)●Since v0.2

# CustomStreamEvent

Custom stream event created by the user.


```
CustomStreamEvent()
```

## Bases

`BaseStreamEvent`

## Attributes

[attribute

event: Literal['on\_custom\_event']

The event type.](/python/langchain-core/runnables/schema/CustomStreamEvent/event)[attribute

name: str

User defined name for the event.](/python/langchain-core/runnables/schema/CustomStreamEvent/name)[attribute

data: Any

The data associated with the event. Free form and can be anything.](/python/langchain-core/runnables/schema/CustomStreamEvent/data)

## Inherited from[BaseStreamEvent](/python/langchain-core/runnables/schema/BaseStreamEvent)

### Attributes

[Arun\_id: str

—

An randomly generated ID to keep track of the execution of the given `Runnable`.](/python/langchain-core/runnables/schema/BaseStreamEvent/run_id)[Atags: NotRequired[list[str]]

—

Tags associated with the `Runnable` that generated this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/tags)[Ametadata: NotRequired[dict[str, Any]]

—

Metadata associated with the `Runnable` that generated this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/metadata)[Aparent\_ids: Sequence[str]

—

A list of the parent IDs associated with this event.](/python/langchain-core/runnables/schema/BaseStreamEvent/parent_ids)


