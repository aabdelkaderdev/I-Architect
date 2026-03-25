<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/FactWithEvidence -->

Classv1.2.13 (latest)●Since v1.0

# FactWithEvidence

Class representing a single statement.

Each fact has a body and a list of sources.
If there are multiple facts make sure to break them apart
such that each one only uses a set of sources that are relevant to it.


```
FactWithEvidence()
```

## Bases

`BaseModel`

## Attributes

[attribute

fact: str](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/FactWithEvidence/fact)[attribute

substring\_quote: list[str]](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/FactWithEvidence/substring_quote)

## Methods

[method

get\_spans

Get spans of the substring quote in the context.](/python/langchain-classic/chains/openai_functions/citation_fuzzy_match/FactWithEvidence/get_spans)


