<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/mapreduce/MapReduceChain/from_params -->

Methodv1.2.13 (latest)●Since v1.0

# from\_params

Construct a map-reduce chain that uses the chain for map and reduce.


```
from_params(
  cls,
  llm: BaseLanguageModel,
  prompt: BasePromptTemplate,
  text_splitter: TextSplitter,
  callbacks: Callbacks = None,
  combine_chain_kwargs: Mapping[str, Any] | None = None,
  reduce_chain_kwargs: Mapping[str, Any] | None = None,
  **kwargs: Any = {}
) -> MapReduceChain
```


