<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/EXAMPLE_OUTPUT -->

Attributev1.2.13 (latest)●Since v1.0

# EXAMPLE\_OUTPUT


```
EXAMPLE_OUTPUT = "First, let's evaluate the final answer. The final uses good reasoning but is wrong. 2,857 divided by 305 is not 17.5.The model should have used the calculator to figure this out. Second does the model use a logical sequence of tools to answer the question?The way model uses the search is not helpful. The model should have used the search tool to figure the width of the US or the height of the statue.The model didn't use the calculator tool and gave an incorrect answer. The search API should be used for current events or specific questions.The tools were not used in a helpful way. The model did not use too many steps to answer the question.The model did not use the appropriate tools to answer the question.\nJudgment: Given the good reasoning in the final answer but otherwise poor performance, we give the model a score of 2.\n\nScore: 2"
```


