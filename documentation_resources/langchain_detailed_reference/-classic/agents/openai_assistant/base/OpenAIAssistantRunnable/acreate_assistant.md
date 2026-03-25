<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/openai_assistant/base/OpenAIAssistantRunnable/acreate_assistant -->

Methodv1.2.13 (latest)●Since v1.0

# acreate\_assistant

Async create an AsyncOpenAI Assistant and instantiate the Runnable.


```
acreate_assistant(
  cls,
  name: str,
  instructions: str,
  tools: Sequence[BaseTool | dict],
  model: str,
  *,
  async_client: openai.AsyncOpenAI | openai.AsyncAzureOpenAI | None = None,
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
| `async_client` | `openai.AsyncOpenAI | openai.AsyncAzureOpenAI | None` | Default:`None`  AsyncOpenAI client. Will create default async\_client if not specified. |
| `**kwargs` | `Any` | Default:`{}`  Additional arguments. |


