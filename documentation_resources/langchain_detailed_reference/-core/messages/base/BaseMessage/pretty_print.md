<!-- Source: https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage/pretty_print -->

Methodv1.2.21 (latest)●Since v0.1

# pretty\_print

Print a pretty representation of the message.


```
pretty_print(
    self,
) -> None
```

**Example:**

```
from langchain_core.messages import AIMessage

msg = AIMessage(content="The capital of France is Paris.")
msg.pretty_print()
```

Results in:

```
================================== Ai Message ==================================

The capital of France is Paris.
```


