<!-- Source: https://reference.langchain.com/python/langchain-core/_api/path/get_relative_path -->

Functionv1.2.21 (latest)●Since v0.1

# get\_relative\_path

Get the path of the file as a relative path to the package directory.


```
get_relative_path(
  file: Path | str,
  *,
  relative_to: Path = PACKAGE_DIR
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `file`\* | `Path | str` | The file path to convert. |
| `relative_to` | `Path` | Default:`PACKAGE_DIR`  The base path to make the file path relative to. |


