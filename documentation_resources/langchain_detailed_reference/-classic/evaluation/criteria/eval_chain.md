<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria/eval_chain -->

Modulev1.2.13 (latest)●Since v1.0

# eval\_chain

## Attributes

[attribute

PROMPT](/python/langchain-classic/evaluation/criteria/prompt/PROMPT)[attribute

PROMPT\_WITH\_REFERENCES](/python/langchain-classic/evaluation/criteria/prompt/PROMPT_WITH_REFERENCES)[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)

## Functions

[function

resolve\_criteria

Resolve the criteria to evaluate.

## Parameters

criteria : CRITERIA\_TYPE
The criteria to evaluate the runs against. It can be:
- a mapping of a criterion name to its description
- a single criterion name present in one of the default criteria
- a single `ConstitutionalPrinciple` instance

## Returns:

Dict[str, str]
A dictionary mapping criterion names to descriptions.

## Examples:

> > > criterion = "relevance"
> > > CriteriaEvalChain.resolve\_criteria(criteria)
> > > {'relevance': 'Is the submission referring to a real quote from the text?'}](/python/langchain-classic/evaluation/criteria/eval_chain/resolve_criteria)

## Classes

[class

ConstitutionalPrinciple

Class for a constitutional principle.](/python/langchain-classic/chains/constitutional_ai/models/ConstitutionalPrinciple)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

Criteria

A Criteria to evaluate.](/python/langchain-classic/evaluation/criteria/eval_chain/Criteria)[class

CriteriaResultOutputParser

A parser for the output of the CriteriaEvalChain.](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaResultOutputParser)[class

CriteriaEvalChain

LLM Chain for evaluating runs against criteria.

## Parameters

llm : BaseLanguageModel
The language model to use for evaluation.
criteria : Union[Mapping[str, str]]
The criteria or rubric to evaluate the runs against. It can be a mapping of
criterion name to its description, or a single criterion name.
prompt : Optional[BasePromptTemplate], default=None
The prompt template to use for generating prompts. If not provided, a
default prompt template will be used based on the value of
`requires_reference`.
requires\_reference : bool, default=False
Whether the evaluation requires a reference text. If `True`, the
`PROMPT_WITH_REFERENCES` template will be used, which includes the
reference labels in the prompt. Otherwise, the `PROMPT` template will be
used, which is a reference-free prompt.
\*\*kwargs : Any
Additional keyword arguments to pass to the `LLMChain` constructor.

## Returns:

CriteriaEvalChain
An instance of the `CriteriaEvalChain` class.

## Examples:

> > > from langchain\_anthropic import ChatAnthropic
> > > from langchain\_classic.evaluation.criteria import CriteriaEvalChain
> > > model = ChatAnthropic(temperature=0)
> > > criteria = {"my-custom-criterion": "Is the submission the most amazing ever?"}
> > > evaluator = CriteriaEvalChain.from\_llm(llm=model, criteria=criteria)
> > > evaluator.evaluate\_strings(
> > > ... prediction="Imagine an ice cream flavor for the color aquamarine",
> > > ... input="Tell me an idea",
> > > ... )
> > > {
> > > 'reasoning': 'Here is my step-by-step reasoning for the given criteria:\n\nThe criterion is: "Is the submission the most amazing ever?" This is a subjective criterion and open to interpretation. The submission suggests an aquamarine-colored ice cream flavor which is creative but may or may not be considered the most amazing idea ever conceived. There are many possible amazing ideas and this one ice cream flavor suggestion may or may not rise to that level for every person. \n\nN',
> > > 'value': 'N',
> > > 'score': 0,
> > > }

> > > from langchain\_openai import ChatOpenAI
> > > from langchain\_classic.evaluation.criteria import LabeledCriteriaEvalChain
> > > model = ChatOpenAI(model="gpt-4", temperature=0)
> > > criteria = "correctness"
> > > evaluator = LabeledCriteriaEvalChain.from\_llm(
> > > ... llm=model,
> > > ... criteria=criteria,
> > > ... )
> > > evaluator.evaluate\_strings(
> > > ... prediction="The answer is 4",
> > > ... input="How many apples are there?",
> > > ... reference="There are 3 apples",
> > > ... )
> > > {
> > > 'score': 0,
> > > 'reasoning': 'The criterion for this task is the correctness of the submission. The submission states that there are 4 apples, but the reference indicates that there are actually 3 apples. Therefore, the submission is not correct, accurate, or factual according to the given criterion.\n\nN',
> > > 'value': 'N',
> > > }](/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain)[class

LabeledCriteriaEvalChain

Criteria evaluation chain that requires references.](/python/langchain-classic/evaluation/criteria/eval_chain/LabeledCriteriaEvalChain)[deprecatedclass

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


