<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/BaseRunManager -->

Classv1.2.21 (latest)●Since v0.1

# BaseRunManager

Base class for run manager (a bound callback manager).


```
BaseRunManager(
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

`RunManagerMixin`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `run_id`\* | `UUID` | The ID of the run. |
| `handlers`\* | `list[BaseCallbackHandler]` | The list of handlers. |
| `inheritable_handlers`\* | `list[BaseCallbackHandler]` | The list of inheritable handlers. |
| `parent_run_id` | `UUID | None` | Default:`None`  The ID of the parent run. |
| `tags` | `list[str] | None` | Default:`None`  The list of tags. |
| `inheritable_tags` | `list[str] | None` | Default:`None`  The list of inheritable tags. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata. |
| `inheritable_metadata` | `dict[str, Any] | None` | Default:`None`  The inheritable metadata. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) |
| handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] |
| inheritable\_handlers | [list](https://docs.python.org/3/library/stdtypes.html#list)[[BaseCallbackHandler](/python/langchain-core/callbacks/base/BaseCallbackHandler)] |
| parent\_run\_id | [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) | None |
| tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| inheritable\_tags | [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |
| metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |
| inheritable\_metadata | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | None |

## Attributes

[attribute

run\_id: run\_id](/python/langchain-core/callbacks/manager/BaseRunManager/run_id)[attribute

handlers: handlers](/python/langchain-core/callbacks/manager/BaseRunManager/handlers)[attribute

inheritable\_handlers: inheritable\_handlers](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_handlers)[attribute

parent\_run\_id: parent\_run\_id](/python/langchain-core/callbacks/manager/BaseRunManager/parent_run_id)[attribute

tags](/python/langchain-core/callbacks/manager/BaseRunManager/tags)[attribute

inheritable\_tags](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_tags)[attribute

metadata](/python/langchain-core/callbacks/manager/BaseRunManager/metadata)[attribute

inheritable\_metadata](/python/langchain-core/callbacks/manager/BaseRunManager/inheritable_metadata)

## Methods

[method

get\_noop\_manager

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


