<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/loading/load_evaluators -->

Functionv1.2.13 (latest)●Since v1.0

# load\_evaluators

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
> > > loaded\_evaluators = load\_evaluators(evaluators, criteria="helpfulness")


```
load_evaluators(
  evaluators: Sequence[EvaluatorType],
  *,
  llm: BaseLanguageModel | None = None,
  config: dict | None = None,
  **kwargs: Any = {}
) -> list[Chain | StringEvaluator]
```


