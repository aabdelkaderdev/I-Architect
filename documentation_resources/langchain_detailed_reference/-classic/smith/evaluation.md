<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation -->

Modulev1.2.13 (latest)●Since v1.0

# evaluation

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
- `InputFormatError`: Exception raised when the input format is incorrect.

## Functions

[function

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

RunEvalConfig

Configuration for a run evaluation.](/python/langchain-classic/smith/evaluation/config/RunEvalConfig)[class

InputFormatError

Raised when the input format is invalid.](/python/langchain-classic/smith/evaluation/runner_utils/InputFormatError)[class

StringRunEvaluatorChain

Evaluate Run and optional examples.](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunEvaluatorChain)

## Modules

[module

name\_generation](/python/langchain-classic/smith/evaluation/name_generation)[module

string\_run\_evaluator

Run evaluator wrapper for string evaluators.](/python/langchain-classic/smith/evaluation/string_run_evaluator)[module

config

Configuration for run evaluators.](/python/langchain-classic/smith/evaluation/config)[module

runner\_utils

Utilities for running language models or Chains over datasets.](/python/langchain-classic/smith/evaluation/runner_utils)[module

progress

A simple progress bar for the console.](/python/langchain-classic/smith/evaluation/progress)


