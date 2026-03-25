<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/question_answering/refine_prompts/refine_template -->

Attributev1.2.13 (latest)●Since v1.0

# refine\_template


```
refine_template = "We have the opportunity to refine the existing answer (
  only if needed
) with some more context below.\n------------\n{context_str}\n------------\nGiven the new context, refine the original answer to better answer the question. If the context isn't useful, return the original answer."
```


