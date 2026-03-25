<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/RunLogPatch -->

Classv1.2.21 (latest)●Since v0.1

# RunLogPatch

Patch to the run log.


```
RunLogPatch(
    self,
    *ops: dict[str, Any] = (),
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `*ops` | `dict[str, Any]` | Default:`()`  The operations to apply to the state. |

## Constructors

[constructor

\_\_init\_\_](/python/langchain-core/tracers/log_stream/RunLogPatch/__init__)

## Attributes

[attribute

ops: list[dict[str, Any]]

List of `JSONPatch` operations, which describe how to create the run state
from an empty dict.

This is the minimal representation of the log, designed to be serialized as JSON and
sent over the wire to reconstruct the log on the other side. Reconstruction of the
state can be done with any JSONPatch-compliant library, see <https://jsonpatch.com>
for more information.](/python/langchain-core/tracers/log_stream/RunLogPatch/ops)


