<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/eval_prompt/template -->

Attributev1.2.13 (latest)●Since v1.0

# template


```
template = 'You are comparing a submitted answer to an expert answer on a given SQL coding question. Here is the data:\n[BEGIN DATA]\n***\n[Question]: {query}\n***\n[Expert]: {answer}\n***\n[Submission]: {result}\n***\n[END DATA]\nCompare the content and correctness of the submitted SQL with the expert answer. Ignore any differences in whitespace, style, or output column names. The submitted answer may either be correct or incorrect. Determine which case applies. First, explain in detail the similarities or differences between the expert answer and the submission, ignoring superficial aspects such as whitespace, style or output column names. Do not state the final answer in your initial explanation. Then, respond with either "CORRECT" or "INCORRECT" (
  without quotes or punctuation
) on its own line. This should correspond to whether the submitted SQL and the expert answer are semantically the same or different, respectively. Then, repeat your final answer on a new line.'
```


