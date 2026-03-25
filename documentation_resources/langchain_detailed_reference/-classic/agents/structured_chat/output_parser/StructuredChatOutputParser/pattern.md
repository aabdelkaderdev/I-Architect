<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/structured_chat/output_parser/StructuredChatOutputParser/pattern -->

Attributev1.2.13 (latest)●Since v1.0

# pattern

Regex pattern to parse the output.


```
pattern: Pattern = re.compile('```(?:json\\s+)?(\\W.*?)```', re.DOTALL)
```


