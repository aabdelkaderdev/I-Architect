<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/github -->

This notebooks shows how you can load issues and pull requests (PRs) for a given repository on [GitHub](https://github.com/). Also shows how you can load github files for a given repository on [GitHub](https://github.com/). We will use the LangChain Python repository as an example.

## [​](#setup-access-token) Setup access token

To access the GitHub API, you need a personal access token - you can set up yours here: [github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta). You can either set this token as the environment variable `GITHUB_PERSONAL_ACCESS_TOKEN` and it will be automatically pulled in, or you can pass it in directly at initialization as the `access_token` named parameter.

Copy

```
# If you haven't set your access token as an environment variable, pass it in here.
from getpass import getpass

ACCESS_TOKEN = getpass()
```

## [​](#load-issues-and-prs) Load issues and PRs

Copy

```
from langchain_community.document_loaders import GitHubIssuesLoader
```

Copy

```
loader = GitHubIssuesLoader(
    repo="langchain-ai/langchain",
    access_token=ACCESS_TOKEN,  # delete/comment out this argument if you've set the access token as an env var.
    creator="UmerHA",
)
```

Let’s load all issues and PRs created by “UmerHA”.
Here’s a list of all filters you can use:

- include\_prs
- milestone
- state
- assignee
- creator
- mentioned
- labels
- sort
- direction
- since

For more info, see [docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues).

Copy

```
docs = loader.load()
```

Copy

```
print(docs[0].page_content)
print(docs[0].metadata)
```

## [​](#only-load-issues) Only load issues

By default, the GitHub API returns considers pull requests to also be issues. To only get ‘pure’ issues (i.e., no pull requests), use `include_prs=False`

Copy

```
loader = GitHubIssuesLoader(
    repo="langchain-ai/langchain",
    access_token=ACCESS_TOKEN,  # delete/comment out this argument if you've set the access token as an env var.
    creator="UmerHA",
    include_prs=False,
)
docs = loader.load()
```

Copy

```
print(docs[0].page_content)
print(docs[0].metadata)
```

## [​](#load-github-file-content) Load GitHub file content

For below code, loads all markdown file in repo `langchain-ai/langchain`

Copy

```
from langchain_community.document_loaders import GithubFileLoader
```

Copy

```
loader = GithubFileLoader(
    repo="langchain-ai/langchain",  # the repo name
    branch="master",  # the branch name
    access_token=ACCESS_TOKEN,
    github_api_url="https://api.github.com",
    file_filter=lambda file_path: file_path.endswith(
        ".md"
    ),  # load all markdowns files.
)
documents = loader.load()
```

example output of one of document:

Copy

```
document.metadata:
    {
      "path": "README.md",
      "sha": "82f1c4ea88ecf8d2dfsfx06a700e84be4",
      "source": "https://github.com/langchain-ai/langchain/blob/master/README.md"
    }
document.content:
    mock content
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/github.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.