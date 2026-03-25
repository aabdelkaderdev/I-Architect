<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/natbot/base/NatBotChain/execute -->

Methodv1.2.13 (latest)●Since v1.0

# execute

Figure out next browser command to run.


```
execute(
    self,
    url: str,
    browser_content: str,
) -> str
```

**Example:**

```
browser_content = "...."
llm_command = natbot.run("www.google.com", browser_content)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url`\* | `str` | URL of the site currently on. |
| `browser_content`\* | `str` | Content of the page as currently displayed by the browser. |


