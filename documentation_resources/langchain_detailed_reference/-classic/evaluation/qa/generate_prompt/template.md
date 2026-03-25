<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/qa/generate_prompt/template -->

Attributev1.2.13 (latest)●Since v1.0

# template


```
template = 'You are a teacher coming up with questions to ask on a quiz.\nGiven the following document, please generate a question and answer based on that document.\n\nExample Format:\n<
  Begin Document
>\n...\n<End Document>\nQUESTION: question here\nANSWER: answer here\n\nThese questions should be detailed and be based explicitly on information in the document. Begin!\n\n<Begin Document>\n{doc}\n<End Document>'
```


