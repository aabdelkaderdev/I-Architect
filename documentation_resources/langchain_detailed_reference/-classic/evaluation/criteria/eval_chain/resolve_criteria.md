<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria/eval_chain/resolve_criteria -->

Functionv1.2.13 (latest)●Since v1.0

# resolve\_criteria

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
> > > {'relevance': 'Is the submission referring to a real quote from the text?'}


```
resolve_criteria(
    criteria: CRITERIA_TYPE | str | None,
) -> dict[str, str]
```


