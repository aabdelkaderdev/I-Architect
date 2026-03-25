<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManagerForToolRun -->

Classv1.2.21 (latest)●Since v0.1

# CallbackManagerForToolRun

Callback manager for tool run.


```
CallbackManagerForToolRun(
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

`ParentRunManager``ToolManagerMixin`

## Methods

[method

on\_tool\_end

Run when the tool ends running.](/python/langchain-core/callbacks/manager/CallbackManagerForToolRun/on_tool_end)[method

on\_tool\_error

Run when tool errors.](/python/langchain-core/callbacks/manager/CallbackManagerForToolRun/on_tool_error)

## Inherited from[ParentRunManager](/python/langchain-core/callbacks/manager/ParentRunManager)

### Methods

[Mget\_child

—

Get a child callback manager.](/python/langchain-core/callbacks/manager/ParentRunManager/get_child)

## Inherited from[RunManager](/python/langchain-core/callbacks/manager/RunManager)

### Methods

[Mon\_text

—

Run when a text is received.](/python/langchain-core/callbacks/manager/RunManager/on_text)[Mon\_retry

—

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

[Mon\_text

—

Run on an arbitrary text.](/python/langchain-core/callbacks/base/RunManagerMixin/on_text)[Mon\_retry

—

Run on a retry event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_retry)[Mon\_custom\_event

—

Override to define a handler for a custom event.](/python/langchain-core/callbacks/base/RunManagerMixin/on_custom_event)


