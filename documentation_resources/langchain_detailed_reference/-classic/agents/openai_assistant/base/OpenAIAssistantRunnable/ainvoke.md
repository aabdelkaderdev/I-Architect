<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/ainvoke -->

Methodv1.2.13 (latest)●Since v1.0

# ainvoke

Async invoke assistant.


```
ainvoke(
  self,
  input: dict,
  config: RunnableConfig | None = None,
  **kwargs: Any = {}
) -> OutputType
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input`\* | `dict` | Runnable input dict that can have: content: User message when starting a new run. thread\_id: Existing thread to use. run\_id: Existing run to use. Should only be supplied when providing the tool output for a required action after an initial invocation. message\_metadata: Metadata to associate with a new message. thread\_metadata: Metadata to associate with new thread. Only relevant when a new thread is created. instructions: Overrides the instructions of the assistant. additional\_instructions: Appends additional instructions. model: Override Assistant model for this run. tools: Override Assistant tools for this run. parallel\_tool\_calls: Allow Assistant to set parallel\_tool\_calls for this run. top\_p: Override Assistant top\_p for this run. temperature: Override Assistant temperature for this run. max\_completion\_tokens: Allow setting max\_completion\_tokens for this run. max\_prompt\_tokens: Allow setting max\_prompt\_tokens for this run. run\_metadata: Metadata to associate with new run. |
| `config` | `RunnableConfig | None` | Default:`None`  Runnable config. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


