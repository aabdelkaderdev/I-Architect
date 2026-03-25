<!-- Source: https://reference.langchain.com/python/langchain-core/_security/_ssrf_protection/validate_safe_url -->

Functionv1.2.21 (latest)●Since v1.2

# validate\_safe\_url

Validate a URL for SSRF protection.

This function validates URLs to prevent Server-Side Request Forgery (SSRF) attacks
by blocking requests to private networks and cloud metadata endpoints.


```
validate_safe_url(
  url: str | AnyHttpUrl,
  *,
  allow_private: bool = False,
  allow_http: bool = True
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `url`\* | `str | AnyHttpUrl` | The URL to validate (string or Pydantic HttpUrl) |
| `allow_private` | `bool` | Default:`False`  If True, allows private IPs and localhost (for development). Cloud metadata endpoints are ALWAYS blocked. |
| `allow_http` | `bool` | Default:`True`  If True, allows both HTTP and HTTPS. If False, only HTTPS. |


