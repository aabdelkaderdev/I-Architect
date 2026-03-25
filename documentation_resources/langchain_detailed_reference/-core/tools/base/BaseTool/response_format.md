<!-- Source: https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/response_format -->

Attributev1.2.21 (latest)●Since v0.2

# response\_format

The tool response format.

If `'content'` then the output of the tool is interpreted as the contents of a
`ToolMessage`. If `'content_and_artifact'` then the output is expected to be a
two-tuple corresponding to the `(content, artifact)` of a `ToolMessage`.


```
response_format: Literal['content', 'content_and_artifact'] = 'content'
```


