<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/markdown/MarkdownHeaderTextSplitter/headers_to_split_on -->

Attributev1.1.1 (latest)●Since v0.0

# headers\_to\_split\_on


```
headers_to_split_on = sorted(
  headers_to_split_on,
  key=(lambda split: len(split[0])),
  reverse=True
)
```


