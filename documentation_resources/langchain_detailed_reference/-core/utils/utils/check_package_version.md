<!-- Source: https://reference.langchain.com/python/langchain-core/utils/utils/check_package_version -->

Functionv1.2.21 (latest)●Since v0.1

# check\_package\_version

Check the version of a package.


```
check_package_version(
  package: str,
  lt_version: str | None = None,
  lte_version: str | None = None,
  gt_version: str | None = None,
  gte_version: str | None = None
) -> None
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `package`\* | `str` | The name of the package. |
| `lt_version` | `str | None` | Default:`None`  The version must be less than this. |
| `lte_version` | `str | None` | Default:`None`  The version must be less than or equal to this. |
| `gt_version` | `str | None` | Default:`None`  The version must be greater than this. |
| `gte_version` | `str | None` | Default:`None`  The version must be greater than or equal to this. |


