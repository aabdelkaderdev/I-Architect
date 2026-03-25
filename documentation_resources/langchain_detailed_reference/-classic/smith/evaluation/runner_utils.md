<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/runner_utils -->

Modulev1.2.13 (latest)●Since v1.0

# runner\_utils

Utilities for running language models or Chains over datasets.

## Attributes

[attribute

logger](/python/langchain-classic/smith/evaluation/runner_utils/logger)

## Functions

[function

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

arun\_on\_dataset

Run on dataset.

Run the Chain or language model on a dataset and store traces
to the specified project name.

For the (usually faster) async version of this function,
see `arun_on_dataset`.](/python/langchain-classic/smith/evaluation/runner_utils/arun_on_dataset)[function

run\_on\_dataset

Run on dataset.

Run the Chain or language model on a dataset and store traces
to the specified project name.

For the (usually faster) async version of this function,
see `arun_on_dataset`.](/python/langchain-classic/smith/evaluation/runner_utils/run_on_dataset)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

EvaluatorType

The types of the evaluators.](/python/langchain-classic/evaluation/schema/EvaluatorType)[class

PairwiseStringEvaluator

Compare the output of two models (or two outputs of the same model).](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

InputFormatError

Raised when the input format is invalid.](/python/langchain-classic/smith/evaluation/runner_utils/InputFormatError)[class

TestResult

A dictionary of the results of a single test run.](/python/langchain-classic/smith/evaluation/runner_utils/TestResult)[class

EvalError

Your architecture raised an error.](/python/langchain-classic/smith/evaluation/runner_utils/EvalError)[class

ChatModelInput

Input for a chat model.](/python/langchain-classic/smith/evaluation/runner_utils/ChatModelInput)

## Type Aliases

[typeAlias

MODEL\_OR\_CHAIN\_FACTORY: Callable[[], Chain | Runnable] | BaseLanguageModel | Callable[[dict], Any] | Runnable | Chain](/python/langchain-classic/smith/evaluation/runner_utils/MODEL_OR_CHAIN_FACTORY)[typeAlias

MCF: Callable[[], Chain | Runnable] | BaseLanguageModel](/python/langchain-classic/smith/evaluation/runner_utils/MCF)

## Modules

[module

smith\_eval

LangSmith evaluation utilities.

This module provides utilities for evaluating Chains and other language model
applications using LangChain evaluators and LangSmith.

For more information on the LangSmith API, see the
[LangSmith API documentation](https://docs.langchain.com/langsmith/home).

**Example**

```
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain
from langchain_classic.smith import EvaluatorType, RunEvalConfig, run_on_dataset

def construct_chain():
    model = ChatOpenAI(temperature=0)
    chain = LLMChain.from_string(model, "What's the answer to {your_input_key}")
    return chain

evaluation_config = RunEvalConfig(
    evaluators=[
        EvaluatorType.QA,  # "Correctness" against a reference answer
        EvaluatorType.EMBEDDING_DISTANCE,
        RunEvalConfig.Criteria("helpfulness"),
        RunEvalConfig.Criteria(
            {
                "fifth-grader-score": "Do you have to be smarter than a fifth "
                "grader to answer this question?"
            }
        ),
    ]
)

client = Client()
run_on_dataset(
    client, "<my_dataset_name>", construct_chain, evaluation=evaluation_config
)
```

**Attributes**

- `arun_on_dataset`: Asynchronous function to evaluate a chain or other LangChain
  component over a dataset.
- `run_on_dataset`: Function to evaluate a chain or other LangChain component over a
  dataset.
- `RunEvalConfig`: Class representing the configuration for running evaluation.
- `StringRunEvaluatorChain`: Class representing a string run evaluator chain.
- `InputFormatError`: Exception raised when the input format is incorrect.](/python/langchain-classic/smith/evaluation)[module

smith\_eval\_config

Configuration for run evaluators.](/python/langchain-classic/smith/evaluation/config)[module

name\_generation](/python/langchain-classic/smith/evaluation/name_generation)[module

progress

A simple progress bar for the console.](/python/langchain-classic/smith/evaluation/progress)


