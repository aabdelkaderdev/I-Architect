<!-- Source: https://reference.langchain.com/python/langchain-classic/memory/summary/SummarizerMixin/apredict_new_summary -->

Methodv1.2.13 (latest)●Since v1.0

# apredict\_new\_summary

Predict a new summary based on the messages and existing summary.


```
apredict_new_summary(
  self,
  messages: list[BaseMessage],
  existing_summary: str
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `messages`\* | `list[BaseMessage]` | List of messages to summarize. |
| `existing_summary`\* | `str` | Existing summary to build upon. |


