<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/loading -->

Modulev1.2.13 (latest)●Since v1.0

# loading

Loading datasets and evaluators.

## Functions

[function

load\_dataset

Load a dataset from the [LangChainDatasets on HuggingFace](https://huggingface.co/LangChainDatasets).](/python/langchain-classic/evaluation/loading/load_dataset)[function

load\_evaluator

Load the requested evaluation chain specified by a string.

## Parameters

evaluator : EvaluatorType
The type of evaluator to load.
llm : BaseLanguageModel, optional
The language model to use for evaluation, by default None
\*\*kwargs : Any
Additional keyword arguments to pass to the evaluator.

## Returns:

Chain
The loaded evaluation chain.

## Examples:

> > > from langchain\_classic.evaluation import load\_evaluator, EvaluatorType
> > > evaluator = load\_evaluator(EvaluatorType.QA)](/python/langchain-classic/evaluation/loading/load_evaluator)[function

load\_evaluators

Load evaluators specified by a list of evaluator types.

## Parameters

evaluators : Sequence[EvaluatorType]
The list of evaluator types to load.
llm : BaseLanguageModel, optional
The language model to use for evaluation, if none is provided, a default
ChatOpenAI gpt-4 model will be used.
config : dict, optional
A dictionary mapping evaluator types to additional keyword arguments,
by default None
\*\*kwargs : Any
Additional keyword arguments to pass to all evaluators.

## Returns:

List[Chain]
The loaded evaluators.

## Examples:

> > > from langchain\_classic.evaluation import load\_evaluators, EvaluatorType
> > > evaluators = [EvaluatorType.QA, EvaluatorType.CRITERIA]
> > > loaded\_evaluators = load\_evaluators(evaluators, criteria="helpfulness")](/python/langchain-classic/evaluation/loading/load_evaluators)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

TrajectoryEvalChain

A chain for evaluating ReAct style agents.

This chain is used to evaluate ReAct style agents by reasoning about
the sequence of actions taken and their outcomes.
Based on the paper "ReAct: Synergizing Reasoning and Acting in Language Models"
(<https://arxiv.org/abs/2210.03629>)

Example:

```
from langchain_classic.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_classic.evaluation import TrajectoryEvalChain
from langchain_classic.tools import tool

@tool
def geography_answers(country: str, question: str) -> str:
    """Very helpful answers to geography questions."""
    return f"{country}? IDK - We may never know {question}."

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = initialize_agent(
    tools=[geography_answers],
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    return_intermediate_steps=True,
)

question = "How many dwell in the largest minor region in Argentina?"
response = agent(question)

eval_chain = TrajectoryEvalChain.from_llm(
    llm=model, agent_tools=[geography_answers], return_reasoning=True
)

result = eval_chain.evaluate_agent_trajectory(
    input=question,
    agent_trajectory=response["intermediate_steps"],
    prediction=response["output"],
    reference="Paris",
)
print(result["score"])  # noqa: T201
# 0
```](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain)[class

PairwiseStringEvalChain

Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain)[class

LabeledPairwiseStringEvalChain

Labeled Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs,
with labeled preferences.](/python/langchain-classic/evaluation/comparison/eval_chain/LabeledPairwiseStringEvalChain)[class

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

Criteria evaluation chain that requires references.](/python/langchain-classic/evaluation/criteria/eval_chain/LabeledCriteriaEvalChain)[class

EmbeddingDistanceEvalChain

Embedding distance evaluation chain.

Use embedding distances to score semantic difference between
a prediction and reference.](/python/langchain-classic/evaluation/embedding_distance/base/EmbeddingDistanceEvalChain)[class

PairwiseEmbeddingDistanceEvalChain

Use embedding distances to score semantic difference between two predictions.

Examples:

> > > chain = PairwiseEmbeddingDistanceEvalChain()
> > > result = chain.evaluate\_string\_pairs(prediction="Hello", prediction\_b="Hi")
> > > print(result)
> > > {'score': 0.5}](/python/langchain-classic/evaluation/embedding_distance/base/PairwiseEmbeddingDistanceEvalChain)[class

ExactMatchStringEvaluator

Compute an exact match between the prediction and the reference.

## Examples:

> > > evaluator = ExactMatchChain()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CTO",
> > > ) # This will return {'score': 1.0}

> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CEO",
> > > ) # This will return {'score': 0.0}](/python/langchain-classic/evaluation/exact_match/base/ExactMatchStringEvaluator)[class

JsonEqualityEvaluator

Json Equality Evaluator.

Evaluate whether the prediction is equal to the reference after
parsing both as JSON.

This evaluator checks if the prediction, after parsing as JSON, is equal
to the reference,
which is also parsed as JSON. It does not require an input string.](/python/langchain-classic/evaluation/parsing/base/JsonEqualityEvaluator)[class

JsonValidityEvaluator

Evaluate whether the prediction is valid JSON.

This evaluator checks if the prediction is a valid JSON string. It does not
require any input or reference.](/python/langchain-classic/evaluation/parsing/base/JsonValidityEvaluator)[class

JsonEditDistanceEvaluator

An evaluator that calculates the edit distance between JSON strings.

This evaluator computes a normalized Damerau-Levenshtein distance between two JSON strings
after parsing them and converting them to a canonical format (i.e., whitespace and key order are normalized).
It can be customized with alternative distance and canonicalization functions.](/python/langchain-classic/evaluation/parsing/json_distance/JsonEditDistanceEvaluator)[class

JsonSchemaEvaluator

An evaluator that validates a JSON prediction against a JSON schema reference.

This evaluator checks if a given JSON prediction conforms to the provided JSON schema.
If the prediction is valid, the score is True (no errors). Otherwise, the score is False (error occurred).](/python/langchain-classic/evaluation/parsing/json_schema/JsonSchemaEvaluator)[class

ContextQAEvalChain

LLM Chain for evaluating QA w/o GT based on context.](/python/langchain-classic/evaluation/qa/eval_chain/ContextQAEvalChain)[class

CotQAEvalChain

LLM Chain for evaluating QA using chain of thought reasoning.](/python/langchain-classic/evaluation/qa/eval_chain/CotQAEvalChain)[class

QAEvalChain

LLM Chain for evaluating question answering.](/python/langchain-classic/evaluation/qa/eval_chain/QAEvalChain)[class

RegexMatchStringEvaluator

Compute a regex match between the prediction and the reference.

## Examples:

> > > evaluator = RegexMatchStringEvaluator(flags=re.IGNORECASE)
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^mindy.\*cto$",
> > > ) # This will return {'score': 1.0} due to the IGNORECASE flag

> > > evaluator = RegexMatchStringEvaluator()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$",
> > > ) # This will return {'score': 0.0}

> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$|^Mindy.\*CTO$",
> > > ) # This will return {'score': 1.0} as the prediction matches the second pattern in the union](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator)[class

EvaluatorType

The types of the evaluators.](/python/langchain-classic/evaluation/schema/EvaluatorType)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

LabeledScoreStringEvalChain

A chain for scoring the output of a model on a scale of 1-10.](/python/langchain-classic/evaluation/scoring/eval_chain/LabeledScoreStringEvalChain)[class

ScoreStringEvalChain

A chain for scoring on a scale of 1-10 the output of a model.](/python/langchain-classic/evaluation/scoring/eval_chain/ScoreStringEvalChain)[class

PairwiseStringDistanceEvalChain

Compute string edit distances between two predictions.](/python/langchain-classic/evaluation/string_distance/base/PairwiseStringDistanceEvalChain)[class

StringDistanceEvalChain

Compute string distances between the prediction and the reference.

## Examples:

> > > from langchain\_classic.evaluation import StringDistanceEvalChain
> > > evaluator = StringDistanceEvalChain()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="Mindy is the CEO",
> > > )

Using the `load_evaluator` function:

> > > from langchain\_classic.evaluation import load\_evaluator
> > > evaluator = load\_evaluator("string\_distance")
> > > evaluator.evaluate\_strings(
> > > prediction="The answer is three",
> > > reference="three",
> > > )](/python/langchain-classic/evaluation/string_distance/base/StringDistanceEvalChain)


