<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/RunLog -->

Classv1.2.21 (latest)●Since v0.1

# RunLog

Run log.


```
RunLog(
    self,
    *ops: dict[str, Any] = (),
    state: RunState,
)
```

## Bases

`RunLogPatch`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `*ops` | `dict[str, Any]` | Default:`()`  The operations to apply to the state. |
| `state`\* | `RunState` | The initial state of the run log. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| state | [RunState](/python/langchain-core/tracers/log_stream/RunState) |

## Attributes

[attribute

state: RunState

Current state of the log, obtained from applying all ops in sequence.](/python/langchain-core/tracers/log_stream/RunLog/state)

## Inherited from[RunLogPatch](/python/langchain-core/tracers/log_stream/RunLogPatch)

### Attributes

[Aops: list[dict[str, Any]]

—

List of `JSONPatch` operations, which describe how to create the run state](/python/langchain-core/tracers/log_stream/RunLogPatch/ops)


