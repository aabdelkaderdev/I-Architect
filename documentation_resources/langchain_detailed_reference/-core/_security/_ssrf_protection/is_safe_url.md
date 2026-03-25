<!-- Source: https://reference.langchain.com/python/langchain-core/_security/_ssrf_protection/is_safe_url -->

Functionv1.2.21 (latest)●Since v1.2

# is\_safe\_url

Check if a URL is safe (non-throwing version of validate\_safe\_url).


```
is_safe_url(
  url: str | AnyHttpUrl,
  *,
  allow_private: bool = False,
  allow_http: bool = True
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url`\* | `str | AnyHttpUrl` | The URL to check |
| `allow_private` | `bool` | Default:`False`  If True, allows private IPs and localhost |
| `allow_http` | `bool` | Default:`True`  If True, allows both HTTP and HTTPS |


