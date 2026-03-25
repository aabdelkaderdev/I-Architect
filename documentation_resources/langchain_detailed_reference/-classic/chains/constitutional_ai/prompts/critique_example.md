<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/prompts/critique_example -->

Attributev1.2.13 (latest)●Since v1.0

# critique\_example


```
critique_example = PromptTemplate(
  template='Human: {input_prompt}\n\nModel: {output_from_model}\n\nCritique Request: {critique_request}\n\nCritique: {critique}',
  input_variables=['input_prompt', 'output_from_model', 'critique_request', 'critique']
)
```


