<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/summarize/refine_prompts/REFINE_PROMPT_TMPL -->

Attributev1.2.13 (latest)●Since v1.0

# REFINE\_PROMPT\_TMPL


```
REFINE_PROMPT_TMPL = "Your job is to produce a final summary.\nWe have provided an existing summary up to a certain point: {existing_answer}\nWe have the opportunity to refine the existing summary (
  only if needed
) with some more context below.\n------------\n{text}\n------------\nGiven the new context, refine the original summary.\nIf the context isn't useful, return the original summary."
```


