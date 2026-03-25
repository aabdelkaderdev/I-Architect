<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/llm_checker/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

Chain for question-answering with self-verification.

## Attributes

[attribute

CHECK\_ASSERTIONS\_PROMPT](/python/langchain-classic/chains/llm_checker/prompt/CHECK_ASSERTIONS_PROMPT)[attribute

CREATE\_DRAFT\_ANSWER\_PROMPT](/python/langchain-classic/chains/llm_checker/prompt/CREATE_DRAFT_ANSWER_PROMPT)[attribute

LIST\_ASSERTIONS\_PROMPT](/python/langchain-classic/chains/llm_checker/prompt/LIST_ASSERTIONS_PROMPT)[attribute

REVISED\_ANSWER\_PROMPT](/python/langchain-classic/chains/llm_checker/prompt/REVISED_ANSWER_PROMPT)

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

LLMCheckerChain

Chain for question-answering with self-verification.](/python/langchain-classic/chains/llm_checker/base/LLMCheckerChain)


