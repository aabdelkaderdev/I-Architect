<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/prompts/revision_example -->

Attributev1.2.13 (latest)●Since v1.0

# revision\_example


```
revision_example = PromptTemplate(
  template='Human: {input_prompt}\n\nModel: {output_from_model}\n\nCritique Request: {critique_request}\n\nCritique: {critique}\n\nRevision Request: {revision_request}\n\nRevision: {revision}',
  input_variables=['input_prompt', 'output_from_model', 'critique_request', 'critique', 'revision_request', 'revision']
)
```


