<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/base/BaseCallbackManager/merge -->

Methodv1.2.21 (latest)●Since v0.2

# merge

Merge the callback manager with another callback manager.

May be overwritten in subclasses.

Primarily used internally within `merge_configs`.


```
merge(
    self,
    other: BaseCallbackManager,
) -> Self
```

**Example:**

```
# Merging two callback managers`
from langchain_core.callbacks.manager import (
    CallbackManager,
    trace_as_chain_group,
)
from langchain_core.callbacks.stdout import StdOutCallbackHandler

manager = CallbackManager(handlers=[StdOutCallbackHandler()], tags=["tag2"])
with trace_as_chain_group("My Group Name", tags=["tag1"]) as group_manager:
    merged_manager = group_manager.merge(manager)
    print(merged_manager.handlers)
    # [
    #    <langchain_core.callbacks.stdout.StdOutCallbackHandler object at ...>,
    #    <langchain_core.callbacks.streaming_stdout.StreamingStdOutCallbackHandler object at ...>,
    # ]

    print(merged_manager.tags)
    #    ['tag2', 'tag1']
```


