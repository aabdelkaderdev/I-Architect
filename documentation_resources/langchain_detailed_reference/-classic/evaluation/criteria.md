<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria -->

Modulev1.2.13 (latest)●Since v1.0

# criteria

Criteria or rubric based evaluators.

These evaluators are useful for evaluating the
output of a language model or chain against
specified criteria or rubric.

## Classes

CriteriaEvalChain : Evaluates the output of a language model or
chain against specified criteria.

## Examples:

Using a predefined criterion:

> > > from langchain\_openai import OpenAI
> > > from langchain\_classic.evaluation.criteria import CriteriaEvalChain

> > > model = OpenAI()
> > > criteria = "conciseness"
> > > chain = CriteriaEvalChain.from\_llm(llm=model, criteria=criteria)
> > > chain.evaluate\_strings(
> > > prediction="The answer is 42.",
> > > reference="42",
> > > input="What is the answer to life, the universe, and everything?",
> > > )

Using a custom criterion:

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
> > > chain.evaluate\_strings(
> > > prediction="The answer to life is 42.",
> > > reference="It's commonly known that the answer to life is 42.",
> > > input="Please summarize the following: The answer to life, the universe, and everything is unknowable.",
> > > )

## Classes

[class

Criteria

A Criteria to evaluate.](/python/langchain-classic/evaluation/criteria/eval_chain/Criteria)[class

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

Criteria evaluation chain that requires references.](/python/langchain-classic/evaluation/criteria/eval_chain/LabeledCriteriaEvalChain)

## Modules

[module

eval\_chain](/python/langchain-classic/evaluation/criteria/eval_chain)[module

prompt](/python/langchain-classic/evaluation/criteria/prompt)


