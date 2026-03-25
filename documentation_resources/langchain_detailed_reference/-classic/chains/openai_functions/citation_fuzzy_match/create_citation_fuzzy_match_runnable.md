<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/create_citation_fuzzy_match_runnable -->

Functionv1.2.13 (latest)●Since v1.0

# create\_citation\_fuzzy\_match\_runnable

Create a citation fuzzy match Runnable.

Example usage:

```
from langchain_classic.chains import create_citation_fuzzy_match_runnable
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

context = "Alice has blue eyes. Bob has brown eyes. Charlie has green eyes."
question = "What color are Bob's eyes?"

chain = create_citation_fuzzy_match_runnable(model)
chain.invoke({"question": question, "context": context})
```


```
create_citation_fuzzy_match_runnable(
    llm: BaseChatModel,
) -> Runnable
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseChatModel` | Language model to use for the chain. Must implement bind\_tools. |


