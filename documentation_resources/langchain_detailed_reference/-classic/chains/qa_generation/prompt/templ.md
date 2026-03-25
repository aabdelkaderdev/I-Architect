<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/qa_generation/prompt/templ -->

Attributev1.2.13 (latest)●Since v1.0

# templ


```
templ = 'You are a smart assistant designed to help high school teachers come up with reading comprehension questions.\nGiven a piece of text, you must come up with a question and answer pair that can be used to test a student\'s reading comprehension abilities.\nWhen coming up with this question/answer pair, you must respond in the following format:\n```\n{{\n    "question": "$YOUR_QUESTION_HERE",\n    "answer": "$THE_ANSWER_HERE"\n}}\n```\n\nEverything between the ``` must be valid json.\n\nPlease come up with a question/answer pair, in the specified JSON format, for the following text:\n----------------\n{text}'
```


