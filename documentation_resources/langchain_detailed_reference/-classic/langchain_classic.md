<!-- Source: https://reference.langchain.com/python/langchain-classic/langchain_classic -->

Modulev1.2.13 (latest)●Since v1.0

# langchain\_classic

Main entrypoint into package.

## Modules

[module

sql\_database](/python/langchain-classic/sql_database)[module

example\_generator](/python/langchain-classic/example_generator)[module

cache](/python/langchain-classic/cache)[module

hub](/python/langchain-classic/hub)[module

base\_memory](/python/langchain-classic/base_memory)[module

requests](/python/langchain-classic/requests)[module

python](/python/langchain-classic/python)[module

input](/python/langchain-classic/input)[module

model\_laboratory](/python/langchain-classic/model_laboratory)[module

serpapi](/python/langchain-classic/serpapi)[module

globals](/python/langchain-classic/globals)[module

formatting](/python/langchain-classic/formatting)[module

env](/python/langchain-classic/env)[module

text\_splitter](/python/langchain-classic/text_splitter)[module

base\_language](/python/langchain-classic/base_language)[module

graphs](/python/langchain-classic/graphs)[module

document\_loaders](/python/langchain-classic/document_loaders)[module

document\_transformers](/python/langchain-classic/document_transformers)[module

prompts](/python/langchain-classic/prompts)[module

chat\_loaders](/python/langchain-classic/chat_loaders)[module

embeddings](/python/langchain-classic/embeddings)[module

docstore](/python/langchain-classic/docstore)[module

vectorstores](/python/langchain-classic/vectorstores)[module

llms](/python/langchain-classic/llms)[module

utilities](/python/langchain-classic/utilities)[module

utils](/python/langchain-classic/utils)[module

callbacks](/python/langchain-classic/callbacks)[module

retrievers](/python/langchain-classic/retrievers)[module

chat\_models](/python/langchain-classic/chat_models)[module

adapters](/python/langchain-classic/adapters)[module

storage](/python/langchain-classic/storage)[module

evaluation](/python/langchain-classic/evaluation)[module

memory](/python/langchain-classic/memory)[module

agents](/python/langchain-classic/agents)[module

output\_parsers](/python/langchain-classic/output_parsers)[module

smith](/python/langchain-classic/smith)[module

runnables](/python/langchain-classic/runnables)[module

load](/python/langchain-classic/load)[module

schema](/python/langchain-classic/schema)[module

chains](/python/langchain-classic/chains)[module

indexes](/python/langchain-classic/indexes)[module

tools](/python/langchain-classic/tools)



Keep here for backwards compatibility.

Keep here for backwards compatibility.

Interface with the [LangChain Hub](https://smith.langchain.com/hub).

**Memory** maintains Chain state, incorporating context from past runs.

This module contains memory abstractions from LangChain v0.0.x.

These abstractions are now deprecated and will be removed in LangChain v1.0.0.

DEPRECATED: Kept for backwards compatibility.

For backwards compatibility.

DEPRECATED: Kept for backwards compatibility.

Experiment with different models.

For backwards compatibility.

Global values and configuration that apply to all of LangChain.

DEPRECATED: Kept for backwards compatibility.

Kept for backwards compatibility.

Deprecated module for BaseLanguageModel class, kept for backwards compatibility.

**Graphs** provide a natural language interface to graph databases.

**Document Loaders** are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

**Document Transformers** are classes to transform Documents.

**Document Transformers** usually used to transform a lot of Documents in a single run.

**Prompt** is the input to the model.

Prompt is often constructed
from multiple components. Prompt classes and functions make constructing and working
with prompts easy.

**Chat Loaders** load chat messages from common communications platforms.

Load chat messages from various
communications platforms such as Facebook Messenger, Telegram, and
WhatsApp. The loaded chat messages can be used for fine-tuning models.

**Embedding models**.

**Embedding models** are wrappers around embedding models
from different APIs and services.

Embedding models can be LLMs or not.

**Docstores** are classes to store and load Documents.

The **Docstore** is a simplified version of the Document Loader.

**Vector store** stores embedded data and performs vector search.

One of the most common ways to store and search over unstructured data is to
embed it and store the resulting embedding vectors, and then query the store
and retrieve the data that are 'most similar' to the embedded query.

**LLMs**.

**LLM** classes provide access to the large language model (**LLM**) APIs and services.

**Utilities** are the integrations with third-part systems and packages.

Other LangChain classes use **Utilities** to interact with third-part systems
and packages.

Utility functions for LangChain.

These functions do not depend on any other LangChain module.

**Callback handlers** allow listening to events in LangChain.

**Retriever** class returns Documents given a text **query**.

It is more general than a vector store. A retriever does not need to be able to
store documents, only to return (or retrieve) it. Vector stores can be used as
the backbone of a retriever, but there are other types of retrievers as well.

**Chat Models** are a variation on language models.

While Chat Models use language models under the hood, the interface they expose
is a bit different. Rather than expose a "text in, text out" API, they expose
an interface where "chat messages" are the inputs and outputs.

Implementations of key-value stores and storage helpers.

Module provides implementations of various key-value stores that conform
to a simple key-value interface.

The primary goal of these storages is to support implementation of caching.

**Memory** maintains Chain state, incorporating context from past runs.

**Agent** is a class that uses an LLM to choose a sequence of actions to take.

In Chains, a sequence of actions is hardcoded. In Agents,
a language model is used as a reasoning engine to determine which actions
to take and in which order.

Agents select and use **Tools** and **Toolkits** for actions.

**OutputParser** classes parse the output of an LLM call.

LangChain **Runnable** and the **LangChain Expression Language (LCEL)**.

The LangChain Expression Language (LCEL) offers a declarative method to build
production-grade programs that harness the power of LLMs.

Programs created using LCEL and LangChain Runnables inherently support
synchronous, asynchronous, batch, and streaming operations.

Support for **async** allows servers hosting the LCEL based programs
to scale better for higher concurrent loads.

**Batch** operations allow for processing multiple inputs in parallel.

**Streaming** of intermediate outputs, as they're being generated, allows for
creating more responsive UX.

This module contains non-core Runnable classes.

Serialization and deserialization.

**Schemas** are the LangChain Base Classes and Interfaces.

**Chains** are easily reusable components linked together.

Chains encode a sequence of calls to components like models, document retrievers,
other Chains, etc., and provide a simple interface to this sequence.

The Chain interface makes it easy to create apps that are:

```
- **Stateful:** add Memory to any Chain to give it state,
- **Observable:** pass Callbacks to a Chain to execute additional functionality,
    like logging, outside the main sequence of component calls,
- **Composable:** combine Chains with other components, including other Chains.
```

**Indexes**.

**Index** is used to avoid writing duplicated content
into the vectostore and to avoid over-writing content if it's unchanged.

Indexes also :

- Create knowledge graphs from data.
- Support indexing workflows from LangChain data loaders to vectorstores.

Importantly, Index keeps on working even if the content being written is derived
via a set of transformations from some source content (e.g., indexing children
documents that were derived from parent documents by chunking.)

**Tools** are classes that an Agent uses to interact with the world.

Each tool has a **description**. Agent uses the description to choose the right
tool for the job.

**Evaluation** chains for grading LLM and Chain outputs.

This module contains off-the-shelf evaluation chains for grading the output of
LangChain primitives such as language models and chains.

**Loading an evaluator**

To load an evaluator, you can use the `load_evaluators <langchain.evaluation.loading.load_evaluators>` or
`load_evaluator <langchain.evaluation.loading.load_evaluator>` functions with the
names of the evaluators to load.

```
from langchain_classic.evaluation import load_evaluator

evaluator = load_evaluator("qa")
evaluator.evaluate_strings(
    prediction="We sold more than 40,000 units last week",
    input="How many units did we sell last week?",
    reference="We sold 32,378 units",
)
```

The evaluator must be one of `EvaluatorType <langchain.evaluation.schema.EvaluatorType>`.

**Datasets**

To load one of the LangChain HuggingFace datasets, you can use the `load_dataset <langchain.evaluation.loading.load_dataset>` function with the
name of the dataset to load.

```
from langchain_classic.evaluation import load_dataset

ds = load_dataset("llm-math")
```

**Some common use cases for evaluation include:**

- Grading the accuracy of a response against ground truth answers: `QAEvalChain <langchain.evaluation.qa.eval_chain.QAEvalChain>`
- Comparing the output of two models: `PairwiseStringEvalChain <langchain.evaluation.comparison.eval_chain.PairwiseStringEvalChain>` or `LabeledPairwiseStringEvalChain <langchain.evaluation.comparison.eval_chain.LabeledPairwiseStringEvalChain>` when there is additionally a reference label.
- Judging the efficacy of an agent's tool usage: `TrajectoryEvalChain <langchain.evaluation.agents.trajectory_eval_chain.TrajectoryEvalChain>`
- Checking whether an output complies with a set of criteria: `CriteriaEvalChain <langchain.evaluation.criteria.eval_chain.CriteriaEvalChain>` or `LabeledCriteriaEvalChain <langchain.evaluation.criteria.eval_chain.LabeledCriteriaEvalChain>` when there is additionally a reference label.
- Computing semantic difference between a prediction and reference: `EmbeddingDistanceEvalChain <langchain.evaluation.embedding_distance.base.EmbeddingDistanceEvalChain>` or between two predictions: `PairwiseEmbeddingDistanceEvalChain <langchain.evaluation.embedding_distance.base.PairwiseEmbeddingDistanceEvalChain>`
- Measuring the string distance between a prediction and reference `StringDistanceEvalChain <langchain.evaluation.string_distance.base.StringDistanceEvalChain>` or between two predictions `PairwiseStringDistanceEvalChain <langchain.evaluation.string_distance.base.PairwiseStringDistanceEvalChain>`

**Low-level API**

These evaluators implement one of the following interfaces:

- `StringEvaluator <langchain.evaluation.schema.StringEvaluator>`: Evaluate a prediction string against a reference label and/or input context.
- `PairwiseStringEvaluator <langchain.evaluation.schema.PairwiseStringEvaluator>`: Evaluate two prediction strings against each other. Useful for scoring preferences, measuring similarity between two chain or llm agents, or comparing outputs on similar inputs.
- `AgentTrajectoryEvaluator <langchain.evaluation.schema.AgentTrajectoryEvaluator>` Evaluate the full sequence of actions taken by an agent.

These interfaces enable easier composability and usage within a higher level evaluation framework.

**LangSmith** utilities.

This module provides utilities for connecting to
[LangSmith](https://docs.langchain.com/langsmith/home).

**Evaluation**

LangSmith helps you evaluate Chains and other language model application components
using a number of LangChain evaluators.
An example of this is shown below, assuming you've created a LangSmith dataset
called `<my_dataset_name>`:

```
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain
from langchain_classic.smith import RunEvalConfig, run_on_dataset

# Chains may have memory. Passing in a constructor function lets the
# evaluation framework avoid cross-contamination between runs.
def construct_chain():
    model = ChatOpenAI(temperature=0)
    chain = LLMChain.from_string(model, "What's the answer to {your_input_key}")
    return chain

# Load off-the-shelf evaluators via config or the EvaluatorType (string or enum)
evaluation_config = RunEvalConfig(
    evaluators=[
        "qa",  # "Correctness" against a reference answer
        "embedding_distance",
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
    client,
    "<my_dataset_name>",
    construct_chain,
    evaluation=evaluation_config,
)
```

You can also create custom evaluators by subclassing the
`StringEvaluator <langchain.evaluation.schema.StringEvaluator>`
or LangSmith's `RunEvaluator` classes.

```
from typing import Optional
from langchain_classic.evaluation import StringEvaluator

class MyStringEvaluator(StringEvaluator):
    @property
    def requires_input(self) -> bool:
        return False

    @property
    def requires_reference(self) -> bool:
        return True

    @property
    def evaluation_name(self) -> str:
        return "exact_match"

    def _evaluate_strings(
        self, prediction, reference=None, input=None, **kwargs
    ) -> dict:
        return {"score": prediction == reference}

evaluation_config = RunEvalConfig(
    custom_evaluators=[MyStringEvaluator()],
)

run_on_dataset(
    client,
    "<my_dataset_name>",
    construct_chain,
    evaluation=evaluation_config,
)
```

**Primary Functions**

- `arun_on_dataset <langchain.smith.evaluation.runner_utils.arun_on_dataset>`:
  Asynchronous function to evaluate a chain, agent, or other LangChain component over
  a dataset.
- `run_on_dataset <langchain.smith.evaluation.runner_utils.run_on_dataset>`:
  Function to evaluate a chain, agent, or other LangChain component over a dataset.
- `RunEvalConfig <langchain.smith.evaluation.config.RunEvalConfig>`:
  Class representing the configuration for running evaluation.
  You can select evaluators by
  `EvaluatorType <langchain.evaluation.schema.EvaluatorType>` or config,
  or you can pass in `custom_evaluators`.