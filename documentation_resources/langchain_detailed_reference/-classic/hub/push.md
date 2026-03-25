<!-- Source: https://reference.langchain.com/python/langchain-classic/hub/push -->

Functionv1.2.13 (latest)●Since v1.0

# push

Push an object to the hub and returns the URL it can be viewed at in a browser.


```
push(
  repo_full_name: str,
  object: Any,
  *,
  api_url: str | None = None,
  api_key: str | None = None,
  parent_commit_hash: str | None = None,
  new_repo_is_public: bool = False,
  new_repo_description: str | None = None,
  readme: str | None = None,
  tags: Sequence[str] | None = None
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `repo_full_name`\* | `str` | The full name of the prompt to push to in the format of `owner/prompt_name` or `prompt_name`. |
| `object`\* | `Any` | The LangChain object to serialize and push to the hub. |
| `api_url` | `str | None` | Default:`None`  The URL of the LangChain Hub API. Defaults to the hosted API service if you have an API key set, or a localhost instance if not. |
| `api_key` | `str | None` | Default:`None`  The API key to use to authenticate with the LangChain Hub API. |
| `parent_commit_hash` | `str | None` | Default:`None`  The commit hash of the parent commit to push to. Defaults to the latest commit automatically. |
| `new_repo_is_public` | `bool` | Default:`False`  Whether the prompt should be public. |
| `new_repo_description` | `str | None` | Default:`None`  The description of the prompt. |
| `readme` | `str | None` | Default:`None`  README content for the repository. |
| `tags` | `Sequence[str] | None` | Default:`None`  Tags to associate with the prompt. |


