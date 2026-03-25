<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/create_assistant -->

Methodv1.2.13 (latest)●Since v1.0

# create\_assistant

Create an OpenAI Assistant and instantiate the Runnable.


```
create_assistant(
  cls,
  name: str,
  instructions: str,
  tools: Sequence[BaseTool | dict],
  model: str,
  *,
  client: openai.OpenAI | openai.AzureOpenAI | None = None,
  **kwargs: Any = {}
) -> OpenAIAssistantRunnable
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `name`\* | `str` | Assistant name. |
| `instructions`\* | `str` | Assistant instructions. |
| `tools`\* | `Sequence[BaseTool | dict]` | Assistant tools. Can be passed in OpenAI format or as BaseTools. |
| `model`\* | `str` | Assistant model to use. |
| `client` | `openai.OpenAI | openai.AzureOpenAI | None` | Default:`None`  OpenAI or AzureOpenAI client. Will create a default OpenAI client if not specified. |
| `kwargs` | `Any` | Default:`{}`  Additional arguments. |


