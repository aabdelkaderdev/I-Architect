<!-- Source: https://reference.langchain.com/python/langchain-core/messages/tool/ToolOutputMixin -->

Classv1.2.21 (latest)●Since v0.3

# ToolOutputMixin

Mixin for objects that tools can return directly.

If a custom BaseTool is invoked with a `ToolCall` and the output of custom code is
not an instance of `ToolOutputMixin`, the output will automatically be coerced to
a string and wrapped in a `ToolMessage`.


```
ToolOutputMixin()
```


