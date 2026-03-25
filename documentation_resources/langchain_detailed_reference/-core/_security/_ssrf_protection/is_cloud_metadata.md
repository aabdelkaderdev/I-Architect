<!-- Source: https://reference.langchain.com/python/langchain-core/_security/_ssrf_protection/is_cloud_metadata -->

Functionv1.2.21 (latest)●Since v1.2

# is\_cloud\_metadata

Check if hostname or IP is a cloud metadata endpoint.


```
is_cloud_metadata(
    hostname: str,
    ip_str: str | None = None,
) -> bool
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `hostname`\* | `str` | Hostname to check |
| `ip_str` | `str | None` | Default:`None`  Optional IP address to check |


