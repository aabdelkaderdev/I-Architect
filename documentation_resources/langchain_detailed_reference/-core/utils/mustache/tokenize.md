<!-- Source: https://reference.langchain.com/python/langchain-core/utils/mustache/tokenize -->

Functionv1.2.21 (latest)●Since v0.1

# tokenize

Tokenize a mustache template.

Tokenizes a mustache template in a generator fashion, using file-like objects. It
also accepts a string containing the template.


```
tokenize(
  template: str,
  def_ldel: str = '{{',
    def_rdel: str = '}}'
) -> Iterator[tuple[str, str]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template`\* | `str` | a file-like object, or a string of a mustache template |
| `def_ldel` | `str` | Default:`'{{'`  The default left delimiter (`'{{'` by default, as in spec compliant mustache) |
| `def_rdel` | `str` | Default:`'}}'`  The default right delimiter (`'}}'` by default, as in spec compliant mustache) |


