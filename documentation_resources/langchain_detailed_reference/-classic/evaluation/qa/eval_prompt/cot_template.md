<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/eval_prompt/cot_template -->

Attributev1.2.13 (latest)●Since v1.0

# cot\_template


```
cot_template = "You are a teacher grading a quiz.\nYou are given a question, the context the question is about, and the student's answer. You are asked to score the student's answer as either CORRECT or INCORRECT, based on the context.\nWrite out in a step by step manner your reasoning to be sure that your conclusion is correct. Avoid simply stating the correct answer at the outset.\n\nExample Format:\nQUESTION: question here\nCONTEXT: context the question is about here\nSTUDENT ANSWER: student's answer here\nEXPLANATION: step by step reasoning here\nGRADE: CORRECT or INCORRECT here\n\nGrade the student answers based ONLY on their factual accuracy. Ignore differences in punctuation and phrasing between the student answer and true answer. It is OK if the student answer contains more information than the true answer, as long as it does not contain any conflicting statements. Begin!\n\nQUESTION: {query}\nCONTEXT: {context}\nSTUDENT ANSWER: {result}\nEXPLANATION:"
```


