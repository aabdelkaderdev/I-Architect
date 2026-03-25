<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/prompts/REVISION_PROMPT -->

Attributev1.2.13 (latest)●Since v1.0

# REVISION\_PROMPT


```
REVISION_PROMPT = FewShotPromptTemplate(
  example_prompt=revision_example,
  examples=examples,
  prefix='Below is a conversation between a human and an AI model.',
  suffix='Human: {input_prompt}\n\nModel: {output_from_model}\n\nCritique Request: {critique_request}\n\nCritique: {critique}\n\nIf the critique does not identify anything worth changing,
  ignore the Revision Request and do not make any revisions. Instead,
  return "No revisions needed".\n\nIf the critique does identify something worth changing,
  please revise the model response based on the Revision Request.\n\nRevision Request: {revision_request}\n\nRevision:',
  example_separator='\n === \n',
  input_variables=['input_prompt', 'output_from_model', 'critique_request', 'critique', 'revision_request']
)
```


