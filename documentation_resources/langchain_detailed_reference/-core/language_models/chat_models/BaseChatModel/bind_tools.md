<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/bind_tools -->

Methodv1.2.21 (latest)●Since v0.1

# bind\_tools

Bind tools to the model.


```
bind_tools(
  self,
  tools: Sequence[builtins.dict[str, Any] | type | Callable | BaseTool],
  *,
  tool_choice: str | None = None,
  **kwargs: Any = {}
) -> Runnable[LanguageModelInput, AIMessage]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `tools`\* | `Sequence[builtins.dict[str, Any] | type | Callable | BaseTool]` | Sequence of tools to bind to the model. |
| `tool_choice` | `str | None` | Default:`None`  The tool to use. If "any" then any tool can be used. |


