<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/AsyncCallbackManager -->

Classv1.2.21 (latest)●Since v0.1

# AsyncCallbackManager

Async callback manager that handles callbacks from LangChain.


```
AsyncCallbackManager(
  self,
  handlers: list[BaseCallbackHandler],
  inheritable_handlers: list[BaseCallbackHandler] | None = None,
  parent_run_id: UUID | None = None,
  *,
  tags: list[str] | None = None,
  inheritable_tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None,
  inheritable_metadata: dict[str, Any] | None = None
)
```

## Bases

`BaseCallbackManager`

## Attributes

[attribute

is\_async: bool

Return whether the handler is async.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/is_async)

## Methods

[method

on\_llm\_start

Run when LLM starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_llm_start)[method

on\_chat\_model\_start

Async run when LLM starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chat_model_start)[method

on\_chain\_start

Async run when chain starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_chain_start)[method

on\_tool\_start

Run when the tool starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_tool_start)[method

on\_custom\_event

Dispatch an adhoc event to the handlers (async version).

This event should NOT be used in any internal LangChain code. The event is meant
specifically for users of the library to dispatch custom events that are
tailored to their application.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_custom_event)[method

on\_retriever\_start

Run when the retriever starts running.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/on_retriever_start)[method

configure

Configure the async callback manager.](/python/langchain-core/callbacks/manager/AsyncCallbackManager/configure)

## Inherited from[BaseCallbackManager](/python/langchain-core/callbacks/base/BaseCallbackManager)

### Attributes

[Ahandlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/handlers)[Ainheritable\_handlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_handlers)[Aparent\_run\_id: UUID | None](/python/langchain-core/callbacks/base/BaseCallbackManager/parent_run_id)[Atags](/python/langchain-core/callbacks/base/BaseCallbackManager/tags)[Ainheritable\_tags](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_tags)[Ametadata](/python/langchain-core/callbacks/base/BaseCallbackManager/metadata)[Ainheritable\_metadata](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_metadata)

### Methods

[Mcopy

—

Return a copy of the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/copy)[Mmerge

—

Merge the callback manager with another callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/merge)[Madd\_handler

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


