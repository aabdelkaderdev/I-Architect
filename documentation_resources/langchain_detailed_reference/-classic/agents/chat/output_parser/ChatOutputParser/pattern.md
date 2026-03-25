<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/chat/output_parser/ChatOutputParser/pattern -->

Attributev1.2.13 (latest)●Since v1.0

# pattern

Regex pattern to parse the output.


```
pattern: Pattern = re.compile('^.*?`{3}(?:json)?\\n(.*?)`{3}.*?$', re.DOTALL)
```


