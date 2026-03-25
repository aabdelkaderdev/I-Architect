<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_summarization_checker/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain for summarization with self-verification.

## Attributes

[attribute

PROMPTS\_DIR](/python/langchain-classic/chains/llm_summarization_checker/base/PROMPTS_DIR)[attribute

logger](/python/langchain-classic/chains/llm_summarization_checker/base/logger)[attribute

CREATE\_ASSERTIONS\_PROMPT](/python/langchain-classic/chains/llm_summarization_checker/base/CREATE_ASSERTIONS_PROMPT)[attribute

CHECK\_ASSERTIONS\_PROMPT](/python/langchain-classic/chains/llm_summarization_checker/base/CHECK_ASSERTIONS_PROMPT)[attribute

REVISED\_SUMMARY\_PROMPT](/python/langchain-classic/chains/llm_summarization_checker/base/REVISED_SUMMARY_PROMPT)[attribute

ARE\_ALL\_TRUE\_PROMPT](/python/langchain-classic/chains/llm_summarization_checker/base/ARE_ALL_TRUE_PROMPT)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

SequentialChain

Chain where the outputs of one chain feed directly into next.](/python/langchain-classic/chains/sequential/SequentialChain)[deprecatedclass

LLMChain

Chain to run queries against LLMs.

This class is deprecated. See below for an example implementation using
LangChain runnables:

```
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(input_variables=["adjective"], template=prompt_template)
model = OpenAI()
chain = prompt | model | StrOutputParser()

chain.invoke("your adjective here")
```](/python/langchain-classic/chains/llm/LLMChain)[deprecatedclass

LLMSummarizationCheckerChain

Chain for question-answering with self-verification.](/python/langchain-classic/chains/llm_summarization_checker/base/LLMSummarizationCheckerChain)


