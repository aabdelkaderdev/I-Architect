<!-- Source: https://reference.langchain.com/python/langchain/agents/middleware/summarization/ContextSize -->

Typev1.2.13 (latest)●Since v1.1

# ContextSize

Union type for context size specifications.

Can be either:

- [`ContextFraction`](/python/langchain/agents/middleware/summarization/ContextFraction): A
  fraction of the model's maximum input tokens.
- [`ContextTokens`](/python/langchain/agents/middleware/summarization/ContextTokens): An absolute
  number of tokens.
- [`ContextMessages`](/python/langchain/agents/middleware/summarization/ContextMessages): An
  absolute number of messages.

Depending on use with `trigger` or `keep` parameters, this type indicates either
when to trigger summarization or how much context to retain.


```
ContextSize = ContextFraction | ContextTokens | ContextMessages
```

**Example:**

```
# ContextFraction
context_size: ContextSize = ("fraction", 0.5)

# ContextTokens
context_size: ContextSize = ("tokens", 3000)

# ContextMessages
context_size: ContextSize = ("messages", 50)
```


