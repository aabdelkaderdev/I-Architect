<!-- Source: https://reference.langchain.com/python/langchain-classic/retrievers/document_compressors/chain_extract_prompt/prompt_template -->

Attributev1.2.13 (latest)●Since v1.0

# prompt\_template


```
prompt_template = 'Given the following question and context, extract any part of the context *AS IS* that is relevant to answer the question. If none of the context is relevant return {no_output_str}.\n\nRemember, *DO NOT* edit the extracted parts of the context.\n\n> Question: {{question}}\n> Context:\n>>>\n{{context}}\n>>>\nExtracted relevant parts:'
```


