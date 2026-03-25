<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/run -->

Methodv1.2.21 (latest)●Since v0.2

# run


```
run(
  self,
  tool_input: str | dict[str, Any],
  verbose
```



:

[bool](https://docs.python.org/3/library/functions.html#bool)

|

None

=

None

,

start\_color

:

[str](https://docs.python.org/3/library/stdtypes.html#str)

|

None

=

'green'

,

color

:

[str](https://docs.python.org/3/library/stdtypes.html#str)

|

None

=

'green'

,

callbacks

:

[Callbacks](/python/langchain-core/callbacks/base/Callbacks)

=

None

,

\*

,

tags

:

[list](https://docs.python.org/3/library/stdtypes.html#list)

[

[str](https://docs.python.org/3/library/stdtypes.html#str)

]

|

None

=

None

,

metadata

:

[dict](https://docs.python.org/3/library/stdtypes.html#dict)

[

[str](https://docs.python.org/3/library/stdtypes.html#str)

,

Any

]

|

None

=

None

,

run\_name

:

[str](https://docs.python.org/3/library/stdtypes.html#str)

|

None

=

None

,

run\_id

:

[uuid](/python/langchain-classic/indexes/_sql_record_manager/UpsertionRecord/uuid)

.

[UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID)

|

None

=

None

,

config

:

[RunnableConfig](/python/langchain-core/runnables/config/RunnableConfig)

|

None

=

None

,

tool\_call\_id

:

[str](https://docs.python.org/3/library/stdtypes.html#str)

|

None

=

None

,

\*\*

kwargs

:

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

=

{

}

)

->

[Any](https://docs.python.org/3/library/typing.html#typing.Any)

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tool_input`\* | `str | dict[str, Any]` | The input to the tool. |
| `verbose` | `bool | None` | Default:`None`  Whether to log the tool's progress. |
| `start_color` | `str | None` | Default:`'green'` |
| `color` | `str | None` | Default:`'green'` |
| `callbacks` | `Callbacks` | Default:`None` |
| `tags` | `list[str] | None` | Default:`None` |
| `metadata` | `dict[str, Any] | None` | Default:`None` |
| `run_name` | `str | None` | Default:`None` |
| `run_id` | `uuid.UUID | None` | Default:`None` |
| `config` | `RunnableConfig | None` | Default:`None` |
| `tool_call_id` | `str | None` | Default:`None` |
| `**kwargs` | `Any` | Default:`{}` |

Run the tool.

The color to use when starting the tool.

The color to use when ending the tool.

Callbacks to be called during tool execution.

Optional list of tags associated with the tool.

Optional metadata associated with the tool.

The name of the run.

The id of the run.

The configuration for the tool.

The id of the tool call.

Keyword arguments to be passed to tool callbacks (event handler)