<!-- Source: https://reference.langchain.com/python/langchain-core/language_models/chat_models/BaseChatModel/output_version -->

Attributev1.2.21 (latest)●Since v1.0

# output\_version

Version of `AIMessage` output format to store in message content.

`AIMessage.content_blocks` will lazily parse the contents of `content` into a
standard format. This flag can be used to additionally store the standard format
in message content, e.g., for serialization purposes.

Supported values:

- `'v0'`: provider-specific format in content (can lazily-parse with
  `content_blocks`)
- `'v1'`: standardized format in content (consistent with `content_blocks`)

Partner packages (e.g.,
[`langchain-openai`](https://pypi.org/project/langchain-openai)) can also use this
field to roll out new content formats in a backward-compatible way.


```
output_version: str | None = Field(default_factory=(from_env('LC_OUTPUT_VERSION', default=None)))
```


