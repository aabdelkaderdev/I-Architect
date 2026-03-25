<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/output_parser/ChatOutputParser/parse -->

Methodv1.2.13 (latest)●Since v1.0

# parse

Parse the output from the agent into an AgentAction or AgentFinish object.


```
parse(
    self,
    text: str,
) -> AgentAction | AgentFinish
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | The text to parse. |


