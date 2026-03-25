<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackManager -->

Classv1.2.21 (latest)●Since v0.1

# BaseCallbackManager

Base callback manager.


```
BaseCallbackManager(
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

`CallbackManagerMixin`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `handlers`\* | `list[BaseCallbackHandler]` | The handlers. |
| `inheritable_handlers` | `list[BaseCallbackHandler] | None` | Default:`None`  The inheritable handlers. |
| `parent_run_id` | `UUID | None` | Default:`None`  The parent run ID. |
| `tags` | `list[str] | None` | Default:`None`  The tags. |
| `inheritable_tags` | `list[str] | None` | Default:`None`  The inheritable tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `inheritable_metadata` | `dict[str, Any] | None` | Default:`None`  The inheritable metadata. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] |
| inheritable\_handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] | None |
| parent\_run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) | None |
| tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| inheritable\_tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |
| inheritable\_metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |

## Attributes

[attribute

handlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/handlers)[attribute

inheritable\_handlers: list[BaseCallbackHandler]](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_handlers)[attribute

parent\_run\_id: UUID | None](/python/langchain-core/callbacks/base/BaseCallbackManager/parent_run_id)[attribute

tags](/python/langchain-core/callbacks/base/BaseCallbackManager/tags)[attribute

inheritable\_tags](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_tags)[attribute

metadata](/python/langchain-core/callbacks/base/BaseCallbackManager/metadata)[attribute

inheritable\_metadata](/python/langchain-core/callbacks/base/BaseCallbackManager/inheritable_metadata)[attribute

is\_async: bool

Whether the callback manager is async.](/python/langchain-core/callbacks/base/BaseCallbackManager/is_async)

## Methods

[method

copy

Return a copy of the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/copy)[method

merge

Merge the callback manager with another callback manager.

May be overwritten in subclasses.

Primarily used internally within `merge_configs`.](/python/langchain-core/callbacks/base/BaseCallbackManager/merge)[method

add\_handler

Add a handler to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_handler)[method

remove\_handler

Remove a handler from the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/remove_handler)[method

set\_handlers

Set handlers as the only handlers on the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/set_handlers)[method

set\_handler

Set handler as the only handler on the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/set_handler)[method

add\_tags

Add tags to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_tags)[method

remove\_tags

Remove tags from the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/remove_tags)[method

add\_metadata

Add metadata to the callback manager.](/python/langchain-core/callbacks/base/BaseCallbackManager/add_metadata)[method

remove\_metadata

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


