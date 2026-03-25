<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/atrace_as_chain_group -->

Functionv1.2.21 (latest)●Since v0.1

# atrace\_as\_chain\_group

Get an async callback manager for a chain group in a context manager.

Useful for grouping different async calls together as a single run even if they
aren't composed in a single chain.


```
atrace_as_chain_group(
  group_name: str,
  callback_manager: AsyncCallbackManager | None = None,
  *,
  inputs: dict[str, Any] | None = None,
  project_name: str | None = None,
  example_id: str | UUID | None = None,
  run_id: UUID | None = None,
  tags: list[str] | None = None,
  metadata: dict[str, Any] | None = None
) -> AsyncGenerator[AsyncCallbackManagerForChainGroup, None]
```

Must have `LANGCHAIN_TRACING_V2` env var set to true to see the trace in
LangSmith.

**Example:**

```
llm_input = "Foo"
async with atrace_as_chain_group(
    "group_name", inputs={"input": llm_input}
) as manager:
    # Use the async callback manager for the chain group
    res = await llm.ainvoke(llm_input, {"callbacks": manager})
    await manager.on_chain_end({"output": res})
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `group_name`\* | `str` | The name of the chain group. |
| `callback_manager` | `AsyncCallbackManager | None` | Default:`None`  The async callback manager to use, which manages tracing and other callback behavior. |
| `inputs` | `dict[str, Any] | None` | Default:`None`  The inputs to the chain group. |
| `project_name` | `str | None` | Default:`None`  The name of the project. |
| `example_id` | `str | UUID | None` | Default:`None`  The ID of the example. |
| `run_id` | `UUID | None` | Default:`None`  The ID of the run. |
| `tags` | `list[str] | None` | Default:`None`  The inheritable tags to apply to all runs. |
| `metadata` | `dict[str, Any] | None` | Default:`None`  The metadata to apply to all runs. |


