<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema/EvaluatorType -->

Classv1.2.13 (latest)●Since v1.0

# EvaluatorType

The types of the evaluators.


```
EvaluatorType()
```

## Bases

`str``Enum`

## Attributes

[attribute

QA: str

Question answering evaluator, which grades answers to questions
directly using an LLM.](/python/langchain-classic/evaluation/schema/EvaluatorType/QA)[attribute

COT\_QA: str

Chain of thought question answering evaluator, which grades
answers to questions using
chain of thought 'reasoning'.](/python/langchain-classic/evaluation/schema/EvaluatorType/COT_QA)[attribute

CONTEXT\_QA: str

Question answering evaluator that incorporates 'context' in the response.](/python/langchain-classic/evaluation/schema/EvaluatorType/CONTEXT_QA)[attribute

PAIRWISE\_STRING: str

The pairwise string evaluator, which predicts the preferred prediction from
between two models.](/python/langchain-classic/evaluation/schema/EvaluatorType/PAIRWISE_STRING)[attribute

SCORE\_STRING: str

The scored string evaluator, which gives a score between 1 and 10
to a prediction.](/python/langchain-classic/evaluation/schema/EvaluatorType/SCORE_STRING)[attribute

LABELED\_PAIRWISE\_STRING: str

The labeled pairwise string evaluator, which predicts the preferred prediction
from between two models based on a ground truth reference label.](/python/langchain-classic/evaluation/schema/EvaluatorType/LABELED_PAIRWISE_STRING)[attribute

LABELED\_SCORE\_STRING: str

The labeled scored string evaluator, which gives a score between 1 and 10
to a prediction based on a ground truth reference label.](/python/langchain-classic/evaluation/schema/EvaluatorType/LABELED_SCORE_STRING)[attribute

AGENT\_TRAJECTORY: str

The agent trajectory evaluator, which grades the agent's intermediate steps.](/python/langchain-classic/evaluation/schema/EvaluatorType/AGENT_TRAJECTORY)[attribute

CRITERIA: str

The criteria evaluator, which evaluates a model based on a
custom set of criteria without any reference labels.](/python/langchain-classic/evaluation/schema/EvaluatorType/CRITERIA)[attribute

LABELED\_CRITERIA: str

The labeled criteria evaluator, which evaluates a model based on a
custom set of criteria, with a reference label.](/python/langchain-classic/evaluation/schema/EvaluatorType/LABELED_CRITERIA)[attribute

STRING\_DISTANCE: str

Compare predictions to a reference answer using string edit distances.](/python/langchain-classic/evaluation/schema/EvaluatorType/STRING_DISTANCE)[attribute

EXACT\_MATCH: str

Compare predictions to a reference answer using exact matching.](/python/langchain-classic/evaluation/schema/EvaluatorType/EXACT_MATCH)[attribute

REGEX\_MATCH: str

Compare predictions to a reference answer using regular expressions.](/python/langchain-classic/evaluation/schema/EvaluatorType/REGEX_MATCH)[attribute

PAIRWISE\_STRING\_DISTANCE: str

Compare predictions based on string edit distances.](/python/langchain-classic/evaluation/schema/EvaluatorType/PAIRWISE_STRING_DISTANCE)[attribute

EMBEDDING\_DISTANCE: str

Compare a prediction to a reference label using embedding distance.](/python/langchain-classic/evaluation/schema/EvaluatorType/EMBEDDING_DISTANCE)[attribute

PAIRWISE\_EMBEDDING\_DISTANCE: str

Compare two predictions using embedding distance.](/python/langchain-classic/evaluation/schema/EvaluatorType/PAIRWISE_EMBEDDING_DISTANCE)[attribute

JSON\_VALIDITY: str

Check if a prediction is valid JSON.](/python/langchain-classic/evaluation/schema/EvaluatorType/JSON_VALIDITY)[attribute

JSON\_EQUALITY: str

Check if a prediction is equal to a reference JSON.](/python/langchain-classic/evaluation/schema/EvaluatorType/JSON_EQUALITY)[attribute

JSON\_EDIT\_DISTANCE: str

Compute the edit distance between two JSON strings after canonicalization.](/python/langchain-classic/evaluation/schema/EvaluatorType/JSON_EDIT_DISTANCE)[attribute

JSON\_SCHEMA\_VALIDATION: str

Check if a prediction is valid JSON according to a JSON schema.](/python/langchain-classic/evaluation/schema/EvaluatorType/JSON_SCHEMA_VALIDATION)


