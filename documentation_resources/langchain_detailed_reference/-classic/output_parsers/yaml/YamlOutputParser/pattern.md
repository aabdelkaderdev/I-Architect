<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/yaml/YamlOutputParser/pattern -->

Attributev1.2.13 (latest)●Since v1.0

# pattern

Regex pattern to match yaml code blocks
within triple backticks with optional yaml or yml prefix.


```
pattern: re.Pattern = re.compile('^```(?:ya?ml)?(?P<yaml>[^`]*)', re.MULTILINE | re.DOTALL)
```


