<!-- Source: https://reference.langchain.com/python/langchain-core/callbacks/manager/CallbackManagerForChainGroup/merge -->

Methodv1.2.21 (latest)●Since v0.2

# merge

Merge the group callback manager with another callback manager.

Overwrites the merge method in the base class to ensure that the parent run
manager is preserved. Keeps the `parent_run_manager` from the current object.


```
merge(
  self: CallbackManagerForChainGroup,
  other: BaseCallbackManager
) -> CallbackManagerForChainGroup
```

**Example:**

```
# Merging two callback managers
from langchain_core.callbacks.manager import (
    CallbackManager,
    trace_as_chain_group,
)
from langchain_core.callbacks.stdout import StdOutCallbackHandler

manager = CallbackManager(handlers=[StdOutCallbackHandler()], tags=["tag2"])
with trace_as_chain_group("My Group Name", tags=["tag1"]) as group_manager:
    merged_manager = group_manager.merge(manager)
    print(type(merged_manager))
    # <class 'langchain_core.callbacks.manager.CallbackManagerForChainGroup'>

    print(merged_manager.handlers)
    # [
    #    <langchain_core.callbacks.stdout.LangChainTracer object at ...>,
    #    <langchain_core.callbacks.streaming_stdout.StdOutCallbackHandler object at ...>,
    # ]

    print(merged_manager.tags)
    #    ['tag2', 'tag1']
```


