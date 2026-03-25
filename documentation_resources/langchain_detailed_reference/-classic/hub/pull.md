<!-- Source: https://reference.langchain.com/python/langchain-classic/hub/pull -->

Functionv1.2.13 (latest)●Since v1.0

# pull

Pull an object from the hub and returns it as a LangChain object.


```
pull(
  owner_repo_commit: str,
  *,
  include_model: bool | None = None,
  api_url: str | None = None,
  api_key: str | None = None
) -> Any
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `owner_repo_commit`\* | `str` | The full name of the prompt to pull from in the format of `owner/prompt_name:commit_hash` or `owner/prompt_name` or just `prompt_name` if it's your own prompt. |
| `include_model` | `bool | None` | Default:`None`  Whether to include the model configuration in the pulled prompt. |
| `api_url` | `str | None` | Default:`None`  The URL of the LangChain Hub API. Defaults to the hosted API service if you have an API key set, or a localhost instance if not. |
| `api_key` | `str | None` | Default:`None`  The API key to use to authenticate with the LangChain Hub API. |


