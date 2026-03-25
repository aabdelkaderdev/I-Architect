<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup -->

Classv1.2.21 (latest)●Since v0.1

# AsyncCallbackManagerForChainGroup

Async callback manager for the chain group.


```
AsyncCallbackManagerForChainGroup(
  self,
  handlers: list[BaseCallbackHandler],
  inheritable_handlers: list[BaseCallbackHandler] | None = None,
  parent_run_id: UUID | None = None,
  *,
  parent_run_manager: AsyncCallbackManagerForChainRun,
  **kwargs: Any = {}
)
```

## Bases

`AsyncCallbackManager`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handlers`\* | `list[BaseCallbackHandler]` | The list of handlers. |
| `inheritable_handlers` | `list[BaseCallbackHandler] | None` | Default:`None`  The list of inheritable handlers. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `parent_run_manager`\* | `AsyncCallbackManagerForChainRun` | The parent run manager. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] |
| inheritable\_handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] | None |
| parent\_run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) | None |
| parent\_run\_manager | [AsyncCallbackManagerForChainRun](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainRun) |

## Attributes

[attribute

parent\_run\_manager: parent\_run\_manager](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/parent_run_manager)[attribute

ended: bool](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/ended)

## Methods

[method

copy

Return a copy the async callback manager.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/copy)[method

merge

Merge the group callback manager with another callback manager.

Overwrites the merge method in the base class to ensure that the parent run
manager is preserved. Keeps the `parent_run_manager` from the current object.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/merge)[method

on\_chain\_end

Run when traced chain group ends.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/on_chain_end)[method

on\_chain\_error

Run when chain errors.](/python/langchain-core/callbacks/manager/AsyncCallbackManagerForChainGroup/on_chain_error)

## Inherited from[AsyncCallbackManager](/python/langchain-core/callbacks/manager/AsyncCallbackManager)

### Attributes

[Ais\_async: bool

—

Return whether the handler is async.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/is_async)

### Methods

[Mon\_llm\_start

—

Run when LLM starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_llm_start)[Mon\_chat\_model\_start

—

Async run when LLM starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chat_model_start)[Mon\_chain\_start

—

Async run when chain starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chain_start)[Mon\_tool\_start

—

Run when the tool starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_tool_start)[Mon\_custom\_event

—

Dispatch an adhoc event to the handlers (async version).](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_custom_event)[Mon\_retriever\_start

—

Run when the retriever starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_retriever_start)[Mconfigure

—

Configure the async callback manager.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/configure)

## Inherited from[BaseCallbackManager](/python/langchain-core/callbacks/base/BaseCallbackManager)

### Attributes

[Ahandlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/handlers)[Ainheritable\_handlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_handlers)[Aparent\_run\_id: UUID | None](/python/langchain-core/callbacks/base/BaseCallbackManager/parent_run_id)[Atags](/python/langchain-core/callbacks/base/BaseCallbackManager/tags)[Ainheritable\_tags](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_tags)[Ametadata](/python/langchain-core/callbacks/base/BaseCallbackManager/metadata)[Ainheritable\_metadata](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_metadata)[Ais\_async: bool

—

Whether the callback manager is async.](/python/langchain-core/callbacks/base/BaseCallbackManager/is_async)

### Methods

[Madd\_handler

—

Add a handler to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_handler)[Mremove\_handler

—

Remove a handler from the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/remove_handler)[Mset\_handlers

—

Set handlers as the only handlers on the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/set_handlers)[Mset\_handler

—

Set handler as the only handler on the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/set_handler)[Madd\_tags

—

Add tags to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_tags)[Mremove\_tags

—

Remove tags from the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/remove_tags)[Madd\_metadata

—

Add metadata to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_metadata)[Mremove\_metadata

—

Remove metadata from the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/remove_metadata)

## Inherited from[CallbackManagerMixin](/python/langchain-core/callbacks/base/CallbackManagerMixin)

### Methods

[Mon\_llm\_start

—

Run when LLM starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_llm_start)[Mon\_chat\_model\_start

—

Run when a chat model starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chat_model_start)[Mon\_retriever\_start

—

Run when the `Retriever` starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_retriever_start)[Mon\_chain\_start

—

Run when a chain starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_chain_start)[Mon\_tool\_start

—

Run when the tool starts running.](/python/langchain-core/callbacks/base/CallbackManagerMixin/on_tool_start)


