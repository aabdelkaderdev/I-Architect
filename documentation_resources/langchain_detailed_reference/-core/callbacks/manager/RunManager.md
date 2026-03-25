<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/RunManager -->

Classv1.2.21 (latest)●Since v0.1

# RunManager

Synchronous run manager.


```
RunManager(
  self,
  *,
  run_id: UUID,
  handlers: list[BaseCallbackHandler],
  inheritable_handlers: list[BaseCallbackHandler],
  parent_run_id: UUID | None = None,
  tags: list[str] | None = None,
  inheritable_tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  inheritable_metadata: dict[str, Any] | None = None
)
```

## Bases

`BaseRunManager`

## Methods

[method

on\_text

Run when a text is received.](/python/langchain-core/callbacks/manager/RunManager/on_text)[method

on\_retry

Run when a retry is received.](/python/langchain-core/callbacks/manager/RunManager/on_retry)

## Inherited from[BaseRunManager](/python/langchain-core/callbacks/manager/BaseRunManager)

### Attributes

[Arun\_id: run\_id](/python/langchain-core/callbacks/manager/BaseRunManager/run_id)[Ahandlers: handlers](/python/langchain-core/callbacks/manager/BaseRunManager/handlers)[Ainheritable\_handlers: inheritable\_handlers](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_handlers)[Aparent\_run\_id: parent\_run\_id](/python/langchain-core/callbacks/manager/BaseRunManager/parent_run_id)[Atags](/python/langchain-core/callbacks/manager/BaseRunManager/tags)[Ainheritable\_tags](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_tags)[Ametadata](/python/langchain-core/callbacks/manager/BaseRunManager/metadata)[Ainheritable\_metadata](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_metadata)

### Methods

[Mget\_noop\_manager

—

Return a manager that doesn't perform any operations.](/python/langchain-core/callbacks/manager/BaseRunManager/get_noop_manager)

## Inherited from[RunManagerMixin](/python/langchain-core/callbacks/base/RunManagerMixin)

### Methods

[Mon\_custom\_event

—

Override to define a handler for a custom event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)


