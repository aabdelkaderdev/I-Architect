<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/loading/load_evaluator -->

Functionv1.2.13 (latest)●Since v1.0

# load\_evaluator

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
> > > evaluator = load\_evaluator(EvaluatorType.QA)


```
load_evaluator(
  evaluator: EvaluatorType,
  *,
  llm: BaseLanguageModel | None = None,
  **kwargs: Any = {}
) -> Chain | StringEvaluator
```


