<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria/eval_chain/CriteriaEvalChain/from_llm -->

Methodv1.2.13 (latest)●Since v1.0

# from\_llm

Create a `CriteriaEvalChain` instance from an llm and criteria.

## Parameters

llm : BaseLanguageModel
The language model to use for evaluation.
criteria : CRITERIA\_TYPE - default=None for "helpfulness"
The criteria to evaluate the runs against. It can be:
- a mapping of a criterion name to its description
- a single criterion name present in one of the default criteria
- a single `ConstitutionalPrinciple` instance
prompt : Optional[BasePromptTemplate], default=None
The prompt template to use for generating prompts. If not provided,
a default prompt template will be used.
\*\*kwargs : Any
Additional keyword arguments to pass to the `LLMChain`
constructor.

## Returns:

CriteriaEvalChain
An instance of the `CriteriaEvalChain` class.

## Examples:

> > > from langchain\_openai import OpenAI
> > > from langchain\_classic.evaluation.criteria import LabeledCriteriaEvalChain
> > > model = OpenAI()
> > > criteria = {
> > > "hallucination": (
> > > "Does this submission contain information"
> > > " not present in the input or reference?"
> > > ),
> > > }
> > > chain = LabeledCriteriaEvalChain.from\_llm(
> > > llm=model,
> > > criteria=criteria,
> > > )


```
from_llm(
  cls,
  llm: BaseLanguageModel,
  criteria: CRITERIA_TYPE | None = None,
  *,
  prompt: BasePromptTemplate | None = None,
  **kwargs: Any = {}
) -> CriteriaEvalChain
```


