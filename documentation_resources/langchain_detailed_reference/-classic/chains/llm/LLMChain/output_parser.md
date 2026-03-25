<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm/LLMChain/output_parser -->

Attributev1.2.13 (latest)●Since v1.0

# output\_parser

Output parser to use.
Defaults to one that takes the most likely string but does not change it
otherwise.


```
output_parser: BaseLLMOutputParser = Field(default_factory=StrOutputParser)
```


