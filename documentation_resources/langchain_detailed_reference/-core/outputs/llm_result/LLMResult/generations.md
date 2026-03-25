<!-- Source: https://reference.langchain.com/python/langchain-core/outputs/llm_result/LLMResult/generations -->

Attributev1.2.21 (latest)●Since v0.1

# generations

Generated outputs.

The first dimension of the list represents completions for different input prompts.

The second dimension of the list represents different candidate generations for a
given prompt.

- When returned from **an LLM**, the type is `list[list[Generation]]`.
- When returned from a **chat model**, the type is `list[list[ChatGeneration]]`.

`ChatGeneration` is a subclass of `Generation` that has a field for a structured
chat message.


```
generations: list[list[Generation | ChatGeneration | GenerationChunk | ChatGenerationChunk]]
```


