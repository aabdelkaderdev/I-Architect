<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/format_scratchpad/xml/format_xml -->

Functionv1.2.13 (latest)●Since v1.0

# format\_xml

Format the intermediate steps as XML.


```
format_xml(
  intermediate_steps: list[tuple[AgentAction, str]],
  *,
  escape_format: Literal['minimal'] | None = 'minimal'
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `intermediate_steps`\* | `list[tuple[AgentAction, str]]` | The intermediate steps. |
| `escape_format` | `Literal['minimal'] | None` | Default:`'minimal'`  The escaping format to use. Currently only 'minimal' is supported, which replaces XML tags with custom delimiters to prevent conflicts. |


