<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/base/Runnable/pick -->

Methodv1.2.21 (latest)●Since v0.1

# pick

Pick keys from the output `dict` of this `Runnable`.

Pick a single key

```
import json

from langchain_core.runnables import RunnableLambda, RunnableMap

as_str = RunnableLambda(str)
as_json = RunnableLambda(json.loads)
chain = RunnableMap(str=as_str, json=as_json)

chain.invoke("[1, 2, 3]")
# -> {"str": "[1, 2, 3]", "json": [1, 2, 3]}

json_only_chain = chain.pick("json")
json_only_chain.invoke("[1, 2, 3]")
# -> [1, 2, 3]
```

Pick a list of keys

```
from typing import Any

import json

from langchain_core.runnables import RunnableLambda, RunnableMap

as_str = RunnableLambda(str)
as_json = RunnableLambda(json.loads)

def as_bytes(x: Any) -> bytes:
    return bytes(x, "utf-8")

chain = RunnableMap(
    str=as_str, json=as_json, bytes=RunnableLambda(as_bytes)
)

chain.invoke("[1, 2, 3]")
# -> {"str": "[1, 2, 3]", "json": [1, 2, 3], "bytes": b"[1, 2, 3]"}

json_and_bytes_chain = chain.pick(["json", "bytes"])
json_and_bytes_chain.invoke("[1, 2, 3]")
# -> {"json": [1, 2, 3], "bytes": b"[1, 2, 3]"}
```


```
pick(
    self,
    keys: str | list[str],
) -> RunnableSerializable[Any, Any]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `keys`\* | `str | list[str]` | A key or list of keys to pick from the output dict. |


