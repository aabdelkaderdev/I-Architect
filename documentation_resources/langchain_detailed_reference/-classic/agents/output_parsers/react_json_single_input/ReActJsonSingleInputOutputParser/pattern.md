<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/output_parsers/react_json_single_input/ReActJsonSingleInputOutputParser/pattern -->

Attributev1.2.13 (latest)●Since v1.0

# pattern

Regex pattern to parse the output.


```
pattern: Pattern = re.compile('^.*?`{3}(?:json)?\\n?(.*?)`{3}.*?$', re.DOTALL)
```


