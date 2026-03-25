<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_with_sources/refine_prompts/DEFAULT_REFINE_PROMPT_TMPL -->

Attributev1.2.13 (latest)●Since v1.0

# DEFAULT\_REFINE\_PROMPT\_TMPL


```
DEFAULT_REFINE_PROMPT_TMPL = "The original question is as follows: {question}\nWe have provided an existing answer, including sources: {existing_answer}\nWe have the opportunity to refine the existing answer(
  only if needed
) with some more context below.\n------------\n{context_str}\n------------\nGiven the new context, refine the original answer to better answer the question. If you do update it, please update the sources as well. If the context isn't useful, return the original answer."
```


