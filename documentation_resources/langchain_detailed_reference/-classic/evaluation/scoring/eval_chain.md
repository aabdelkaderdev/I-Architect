<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/scoring/eval_chain -->

Modulev1.2.13 (latest)●Since v1.0

# eval\_chain

Base classes for scoring the output of a model on a scale of 1-10.

## Attributes

[attribute

CRITERIA\_INSTRUCTIONS: str](/python/langchain-classic/evaluation/scoring/prompt/CRITERIA_INSTRUCTIONS)[attribute

DEFAULT\_CRITERIA: str](/python/langchain-classic/evaluation/scoring/prompt/DEFAULT_CRITERIA)[attribute

SCORING\_TEMPLATE](/python/langchain-classic/evaluation/scoring/prompt/SCORING_TEMPLATE)[attribute

SCORING\_TEMPLATE\_WITH\_REFERENCE](/python/langchain-classic/evaluation/scoring/prompt/SCORING_TEMPLATE_WITH_REFERENCE)[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)[attribute

logger](/python/langchain-classic/evaluation/scoring/eval_chain/logger)

## Functions

[function

resolve\_criteria

Resolve the criteria for the pairwise evaluator.](/python/langchain-classic/evaluation/scoring/eval_chain/resolve_criteria)

## Classes

[class

ConstitutionalPrinciple

Class for a constitutional principle.](/python/langchain-classic/chains/constitutional_ai/models/ConstitutionalPrinciple)[class

Criteria

A Criteria to evaluate.](/python/langchain-classic/evaluation/criteria/eval_chain/Criteria)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

ScoreStringResultOutputParser

A parser for the output of the ScoreStringEvalChain.](/python/langchain-classic/evaluation/scoring/eval_chain/ScoreStringResultOutputParser)[class

ScoreStringEvalChain

A chain for scoring on a scale of 1-10 the output of a model.](/python/langchain-classic/evaluation/scoring/eval_chain/ScoreStringEvalChain)[class

LabeledScoreStringEvalChain

A chain for scoring the output of a model on a scale of 1-10.](/python/langchain-classic/evaluation/scoring/eval_chain/LabeledScoreStringEvalChain)[deprecatedclass

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


