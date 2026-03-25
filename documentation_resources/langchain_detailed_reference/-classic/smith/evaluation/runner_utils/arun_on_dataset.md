<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/runner_utils/arun_on_dataset -->

Functionv1.2.13 (latest)●Since v1.0

# arun\_on\_dataset

Run on dataset.

Run the Chain or language model on a dataset and store traces
to the specified project name.

For the (usually faster) async version of this function,
see `arun_on_dataset`.


```
arun_on_dataset(
  client: Client | None,
  dataset_name: str,
  llm_or_chain_factory: MODEL_OR_CHAIN_FACTORY,
  *,
  evaluation: smith_eval.RunEvalConfig | None = None,
  dataset_version: datetime | str | None = None,
  concurrency_level: int = 5,
  project_name: str | None = None,
  project_metadata: dict[str, Any] | None = None,
  verbose: bool = False,
  revision_id: str | None = None,
  **kwargs: Any = {}
) -> dict[str, Any]
```

Examples:

```
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain
from langchain_classic.smith import smith_eval.RunEvalConfig, run_on_dataset

# Chains may have memory. Passing in a constructor function lets the
# evaluation framework avoid cross-contamination between runs.
def construct_chain():
    model = ChatOpenAI(temperature=0)
    chain = LLMChain.from_string(
        model,
        "What's the answer to {your_input_key}"
    )
    return chain

# Load off-the-shelf evaluators via config or the EvaluatorType (string or enum)
evaluation_config = smith_eval.RunEvalConfig(
    evaluators=[
        "qa",  # "Correctness" against a reference answer
        "embedding_distance",
        smith_eval.RunEvalConfig.Criteria("helpfulness"),
        smith_eval.RunEvalConfig.Criteria({
            "fifth-grader-score": "Do you have to be smarter than a fifth "
            "grader to answer this question?"
        }),
    ]
)

client = Client()
await arun_on_dataset(
    client,
    dataset_name="<my_dataset_name>",
    llm_or_chain_factory=construct_chain,
    evaluation=evaluation_config,
)
```

You can also create custom evaluators by subclassing the `StringEvaluator or LangSmith's` RunEvaluator` classes.

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

evaluation_config = smith_eval.RunEvalConfig(
    custom_evaluators=[MyStringEvaluator()],
)

await arun_on_dataset(
    client,
    dataset_name="<my_dataset_name>",
    llm_or_chain_factory=construct_chain,
    evaluation=evaluation_config,
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `dataset_name`\* | `str` | Name of the dataset to run the chain on. |
| `llm_or_chain_factory`\* | `MODEL_OR_CHAIN_FACTORY` | Language model or Chain constructor to run over the dataset. The Chain constructor is used to permit independent calls on each example without carrying over state. |
| `evaluation` | `smith_eval.RunEvalConfig | None` | Default:`None`  Configuration for evaluators to run on the results of the chain. |
| `dataset_version` | `datetime | str | None` | Default:`None`  Optional version of the dataset. |
| `concurrency_level` | `int` | Default:`5`  The number of async tasks to run concurrently. |
| `project_name` | `str | None` | Default:`None`  Name of the project to store the traces in. Defaults to `{dataset_name}-{chain class name}-{datetime}`. |
| `project_metadata` | `dict[str, Any] | None` | Default:`None`  Optional metadata to add to the project. Useful for storing information the test variant. (prompt version, model version, etc.) |
| `client`\* | `Client | None` | LangSmith client to use to access the dataset and to log feedback and run traces. |
| `verbose` | `bool` | Default:`False`  Whether to print progress. |
| `revision_id` | `str | None` | Default:`None`  Optional revision identifier to assign this test run to track the performance of different versions of your system. |
| `**kwargs` | `Any` | Default:`{}`  Should not be used, but is provided for backwards compatibility. |


