<!-- Source: https://reference.langchain.com/python/langchain-core/utils/mustache/render -->

Functionv1.2.21 (latest)●Since v0.1

# render

Render a mustache template.

Renders a mustache template with a data scope and inline partial capability.


```
render(
  template: str | list[tuple[str, str]] = '',
  data: Mapping[str, Any] = EMPTY_DICT,
  partials_dict: Mapping[str, str] = EMPTY_DICT,
  padding: str = '',
  def_ldel: str = '{{',
    def_rdel: str = '}}',
  scopes: Scopes | None = None,
  warn: bool = False,
  keep: bool = False
) -> str
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `template` | `str | list[tuple[str, str]]` | Default:`''`  A file-like object or a string containing the template. |
| `data` | `Mapping[str, Any]` | Default:`EMPTY_DICT`  A python dictionary with your data scope. |
| `partials_dict` | `Mapping[str, str]` | Default:`EMPTY_DICT`  A python dictionary which will be search for partials before the filesystem is.  `{'include': 'foo'}` is the same as a file called include.mustache (defaults to `{}`). |
| `padding` | `str` | Default:`''`  This is for padding partials, and shouldn't be used (but can be if you really want to). |
| `def_ldel` | `str` | Default:`'{{'`  The default left delimiter  (`'{{'` by default, as in spec compliant mustache). |
| `def_rdel` | `str` | Default:`'}}'`  The default right delimiter  (`'}}'` by default, as in spec compliant mustache). |
| `scopes` | `Scopes | None` | Default:`None`  The list of scopes that `get_key` will look through. |
| `warn` | `bool` | Default:`False`  Log a warning when a template substitution isn't found in the data |
| `keep` | `bool` | Default:`False`  Keep unreplaced tags when a substitution isn't found in the data. |


