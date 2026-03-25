<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/prompts/CRITIQUE_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# CRITIQUE\_PROMPT


```
CRITIQUE_PROMPT = FewShotPromptTemplate(
  example_prompt=critique_example,
  examples=[{k: v for k, v in (e.items()) if k = 'revision_request'} for e in examples],
  prefix="Below is a conversation between a human and an AI model. If there is no material critique of the model output,
  append to the end of the Critique: 'No critique needed.' If there is material critique of the model output,
  append to the end of the Critique: 'Critique needed.'",
  suffix='Human: {input_prompt}\nModel: {output_from_model}\n\nCritique Request: {critique_request}\n\nCritique:',
  example_separator='\n === \n',
  input_variables=['input_prompt', 'output_from_model', 'critique_request']
)
```


