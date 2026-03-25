<!-- Source: https://reference.langchain.com/python/langchain-text-splitters/jsx/JSFrameworkTextSplitter/split_text -->

Methodv1.1.1 (latest)●Since v0.3

# split\_text

Split text into chunks.

This method splits the text into chunks by:

- Extracting unique opening component tags using regex
- Creating separators list with extracted tags and JS separators
- Splitting the text using the separators by calling the parent class method


```
split_text(
    self,
    text: str,
) -> list[str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `text`\* | `str` | String containing code to split |


