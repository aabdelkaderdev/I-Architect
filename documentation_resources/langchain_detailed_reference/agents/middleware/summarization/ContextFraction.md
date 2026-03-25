<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextFraction -->

Attributev1.2.13 (latest)●Since v1.1

# ContextFraction

Fraction of model's maximum input tokens.


```
ContextFraction = tuple[Literal['fraction'], float]
```

**Example:**

To specify 50% of the model's max input tokens:

```
("fraction", 0.5)
```


