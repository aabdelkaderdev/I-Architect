<!-- Source: https://reference.langchain.com/python/langchain-tests/unit_tests/tools/ToolsUnitTests/test_has_name -->

Methodv1.1.4 (latest)●Since v1.1

# test\_has\_name


```
test_has_name(
    self,
    tool: BaseTool,
) -> None
```



Tests that the tool has a name attribute to pass to chat models.

If this fails, add a `name` parameter to your tool.