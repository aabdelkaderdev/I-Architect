<!-- Source: https://reference.langchain.com/python/langchain-core/_import_utils/import_attr -->

Functionv1.2.21 (latest)●Since v0.3

# import\_attr

Import an attribute from a module located in a package.

This utility function is used in custom `__getattr__` methods within `__init__.py`
files to dynamically import attributes.


```
import_attr(
  attr_name: str,
  module_name: str | None,
  package: str | None
) -> object
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `attr_name`\* | `str` | The name of the attribute to import. |
| `module_name`\* | `str | None` | The name of the module to import from.  If `None`, the attribute is imported from the package itself. |
| `package`\* | `str | None` | The name of the package where the module is located. |


