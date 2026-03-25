<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/astream_log -->

Methodv1.2.21 (latest)●Since v0.1

# astream\_log

Stream all output from a `Runnable`, as reported to the callback system.

This includes all inner runs of LLMs, Retrievers, Tools, etc.

Output is streamed as Log objects, which include a list of
Jsonpatch ops that describe how the state of the run has changed in each
step, and the final state of the run.

The Jsonpatch ops can be applied in order to construct state.


```
astream_log(
  self,
  input: Any,
  config: RunnableConfig | None = None,
  *,
  diff: bool = True,
  with_streamed_output_list: bool = True,
  include_names: Sequence[str] | None = None,
  include_types: Sequence[str] | None = None,
  include_tags: Sequence[str] | None = None,
  exclude_names: Sequence[str] | None = None,
  exclude_types: Sequence[str] | None = None,
  exclude_tags: Sequence[str] | None = None,
  **kwargs: Any = {}
) -> AsyncIterator[RunLogPatch] | AsyncIterator[RunLog]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `Any` | The input to the `Runnable`. |
| `config` | `RunnableConfig | None` | Default:`None`  The config to use for the `Runnable`. |
| `diff` | `bool` | Default:`True`  Whether to yield diffs between each step or the current state. |
| `with_streamed_output_list` | `bool` | Default:`True`  Whether to yield the `streamed_output` list. |
| `include_names` | `Sequence[str] | None` | Default:`None`  Only include logs with these names. |
| `include_types` | `Sequence[str] | None` | Default:`None`  Only include logs with these types. |
| `include_tags` | `Sequence[str] | None` | Default:`None`  Only include logs with these tags. |
| `exclude_names` | `Sequence[str] | None` | Default:`None`  Exclude logs with these names. |
| `exclude_types` | `Sequence[str] | None` | Default:`None`  Exclude logs with these types. |
| `exclude_tags` | `Sequence[str] | None` | Default:`None`  Exclude logs with these tags. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments to pass to the `Runnable`. |


