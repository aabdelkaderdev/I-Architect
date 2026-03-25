<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/types/ModelRequest/override -->

Methodv1.2.13 (latest)●Since v1.0

# override

Replace the request with a new request with the given overrides.

Returns a new `ModelRequest` instance with the specified attributes replaced.

This follows an immutable pattern, leaving the original request unchanged.


```
override(
  self,
  **overrides: Unpack[_ModelRequestOverrides] = {}
) -> ModelRequest[ContextT]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**overrides` | `Unpack[_ModelRequestOverrides]` | Default:`{}`  Keyword arguments for attributes to override.  Supported keys:   - `model`: `BaseChatModel` instance - `system_prompt`: deprecated, use `system_message` instead - `system_message`: `SystemMessage` instance - `messages`: `list` of messages - `tool_choice`: Tool choice configuration - `tools`: `list` of available tools - `response_format`: Response format specification - `model_settings`: Additional model settings - `state`: Agent state dictionary |


