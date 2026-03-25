<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_summarization_checker -->

Modulev1.2.13 (latest)●Since v1.0

# llm\_summarization\_checker

Summarization checker chain for verifying accuracy of text generation.

Chain that tries to verify the accuracy of text generation by splitting it into a
list of facts, then checking if those facts are true or not, and rewriting
the text to make it more truthful. It will repeat this loop until it hits `max_tries` or
gets to a "true" output.

## Modules

[module

base

Chain for summarization with self-verification.](/python/langchain-classic/chains/llm_summarization_checker/base)


