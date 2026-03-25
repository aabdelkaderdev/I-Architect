<!-- Source: https://reference.langchain.com/python/langchain-core/utils/function_calling/tool_example_to_messages -->

Functionv1.2.21 (latest)●Since v0.1

# tool\_example\_to\_messages

Convert an example into a list of messages that can be fed into an LLM.

This code is an adapter that converts a single example to a list of messages
that can be fed into a chat model.

The list of messages per example by default corresponds to:

1. `HumanMessage`: contains the content from which content should be extracted.
2. `AIMessage`: contains the extracted information from the model
3. `ToolMessage`: contains confirmation to the model that the model requested a
   tool correctly.

If `ai_response` is specified, there will be a final `AIMessage` with that
response.

The `ToolMessage` is required because some chat models are hyper-optimized for
agents rather than for an extraction use case.


```
tool_example_to_messages(
  input: str,
  tool_calls: list[BaseModel],
  tool_outputs: list[str] | None = None,
  *,
  ai_response: str | None = None
) -> list[BaseMessage]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `str` | The user input |
| `tool_calls`\* | `list[BaseModel]` | Tool calls represented as Pydantic BaseModels |
| `tool_outputs` | `list[str] | None` | Default:`None`  Tool call outputs.  Does not need to be provided.  If not provided, a placeholder value will be inserted. |
| `ai_response` | `str | None` | Default:`None`  If provided, content for a final `AIMessage`. |


