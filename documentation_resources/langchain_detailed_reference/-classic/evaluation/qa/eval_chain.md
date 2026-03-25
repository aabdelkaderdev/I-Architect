<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/eval_chain -->

Modulev1.2.13 (latest)●Since v1.0

# eval\_chain

LLM Chains for evaluating question answering.

## Attributes

[attribute

CONTEXT\_PROMPT](/python/langchain-classic/evaluation/qa/eval_prompt/CONTEXT_PROMPT)[attribute

COT\_PROMPT](/python/langchain-classic/evaluation/qa/eval_prompt/COT_PROMPT)[attribute

PROMPT](/python/langchain-classic/evaluation/qa/eval_prompt/PROMPT)[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)

## Classes

[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

QAEvalChain

LLM Chain for evaluating question answering.](/python/langchain-classic/evaluation/qa/eval_chain/QAEvalChain)[class

ContextQAEvalChain

LLM Chain for evaluating QA w/o GT based on context.](/python/langchain-classic/evaluation/qa/eval_chain/ContextQAEvalChain)[class

CotQAEvalChain

LLM Chain for evaluating QA using chain of thought reasoning.](/python/langchain-classic/evaluation/qa/eval_chain/CotQAEvalChain)[deprecatedclass

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
```](/python/langchain-classic/chains/llm/LLMChain)


