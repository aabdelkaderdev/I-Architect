<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/tags -->

Attributev1.2.21 (latest)●Since v0.2

# tags

Optional list of tags associated with the tool.

These tags will be associated with each call to this tool,
and passed as arguments to the handlers defined in `callbacks`.

You can use these to, e.g., identify a specific instance of a tool with its use
case.


```
tags: list[str] | None = None
```


