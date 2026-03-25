<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage/artifact -->

Attributev1.2.21 (latest)●Since v0.2

# artifact

Artifact of the Tool execution which is not meant to be sent to the model.

Should only be specified if it is different from the message content, e.g. if only
a subset of the full tool output is being passed as message content but the full
output is needed in other parts of the code.


```
artifact: Any = None
```


