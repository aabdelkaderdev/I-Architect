<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/xml/XMLAgentOutputParser/escape_format -->

Attributev1.2.13 (latest)●Since v1.0

# escape\_format

The format to use for escaping XML characters.

minimal - uses custom delimiters to replace XML tags within content,
preventing parsing conflicts. This is the only supported format currently.

None - no escaping is applied, which may lead to parsing conflicts.


```
escape_format: Literal['minimal'] | None = Field(default='minimal')
```


