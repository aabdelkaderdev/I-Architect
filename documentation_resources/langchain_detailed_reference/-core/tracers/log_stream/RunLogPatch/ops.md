<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/log_stream/RunLogPatch/ops -->

Attributev1.2.21 (latest)●Since v0.1

# ops

List of `JSONPatch` operations, which describe how to create the run state
from an empty dict.

This is the minimal representation of the log, designed to be serialized as JSON and
sent over the wire to reconstruct the log on the other side. Reconstruction of the
state can be done with any JSONPatch-compliant library, see <https://jsonpatch.com>
for more information.


```
ops: list[dict[str, Any]] = list(ops)
```


