<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/criteria/prompt/template -->

Attributev1.2.13 (latest)●Since v1.0

# template


```
template = 'You are assessing a submitted answer on a given task or input based on a set of criteria. Here is the data:\n[BEGIN DATA]\n***\n[Input]: {input}\n***\n[Submission]: {output}\n***\n[Criteria]: {criteria}\n***\n[Reference]: {reference}\n***\n[END DATA]\nDoes the submission meet the Criteria? First, write out in a step by step manner your reasoning about each criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character "Y" or "N" (
  without quotes or punctuation
) on its own line corresponding to the correct answer of whether the submission meets all criteria. At the end, repeat just the letter again by itself on a new line.'
```


