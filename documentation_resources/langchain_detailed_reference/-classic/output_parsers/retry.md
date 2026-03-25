<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/retry -->

Modulev1.2.13 (latest)●Since v1.0

# retry

## Attributes

[attribute

NAIVE\_COMPLETION\_RETRY: str](/python/langchain-classic/output_parsers/retry/NAIVE_COMPLETION_RETRY)[attribute

NAIVE\_COMPLETION\_RETRY\_WITH\_ERROR: str](/python/langchain-classic/output_parsers/retry/NAIVE_COMPLETION_RETRY_WITH_ERROR)[attribute

NAIVE\_RETRY\_PROMPT](/python/langchain-classic/output_parsers/retry/NAIVE_RETRY_PROMPT)[attribute

NAIVE\_RETRY\_WITH\_ERROR\_PROMPT](/python/langchain-classic/output_parsers/retry/NAIVE_RETRY_WITH_ERROR_PROMPT)[attribute

T](/python/langchain-classic/output_parsers/retry/T)

## Classes

[class

RetryOutputParserRetryChainInput

Retry chain input for RetryOutputParser.](/python/langchain-classic/output_parsers/retry/RetryOutputParserRetryChainInput)[class

RetryWithErrorOutputParserRetryChainInput

Retry chain input for RetryWithErrorOutputParser.](/python/langchain-classic/output_parsers/retry/RetryWithErrorOutputParserRetryChainInput)[class

RetryOutputParser

Wrap a parser and try to fix parsing errors.

Does this by passing the original prompt and the completion to another
LLM, and telling it the completion did not satisfy criteria in the prompt.](/python/langchain-classic/output_parsers/retry/RetryOutputParser)[class

RetryWithErrorOutputParser

Wrap a parser and try to fix parsing errors.

Does this by passing the original prompt, the completion, AND the error
that was raised to another language model and telling it that the completion
did not work, and raised the given error. Differs from RetryOutputParser
in that this implementation provides the error that was raised back to the
LLM, which in theory should give it more information on how to fix it.](/python/langchain-classic/output_parsers/retry/RetryWithErrorOutputParser)


