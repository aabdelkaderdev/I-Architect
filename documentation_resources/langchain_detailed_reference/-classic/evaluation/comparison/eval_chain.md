<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison/eval_chain -->

Modulev1.2.13 (latest)●Since v1.0

# eval\_chain

Base classes for comparing the output of two models.

## Attributes

[attribute

COMPARISON\_TEMPLATE](/python/langchain-classic/evaluation/comparison/prompt/COMPARISON_TEMPLATE)[attribute

COMPARISON\_TEMPLATE\_WITH\_REFERENCE](/python/langchain-classic/evaluation/comparison/prompt/COMPARISON_TEMPLATE_WITH_REFERENCE)[attribute

CRITERIA\_INSTRUCTIONS: str](/python/langchain-classic/evaluation/comparison/prompt/CRITERIA_INSTRUCTIONS)[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)[attribute

logger](/python/langchain-classic/evaluation/comparison/eval_chain/logger)

## Functions

[function

resolve\_pairwise\_criteria

Resolve the criteria for the pairwise evaluator.](/python/langchain-classic/evaluation/comparison/eval_chain/resolve_pairwise_criteria)

## Classes

[class

ConstitutionalPrinciple

Class for a constitutional principle.](/python/langchain-classic/chains/constitutional_ai/models/ConstitutionalPrinciple)[class

Criteria

A Criteria to evaluate.](/python/langchain-classic/evaluation/criteria/eval_chain/Criteria)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

PairwiseStringEvaluator

Compare the output of two models (or two outputs of the same model).](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)[class

PairwiseStringResultOutputParser

A parser for the output of the PairwiseStringEvalChain.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringResultOutputParser)[class

PairwiseStringEvalChain

Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain)[class

LabeledPairwiseStringEvalChain

Labeled Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs,
with labeled preferences.](/python/langchain-classic/evaluation/comparison/eval_chain/LabeledPairwiseStringEvalChain)[deprecatedclass

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

## Type Aliases

[typeAlias

CRITERIA\_TYPE: Mapping[str, str] | Criteria | ConstitutionalPrinciple](/python/langchain-classic/evaluation/criteria/eval_chain/CRITERIA_TYPE)


