<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/constitutional_ai/base/ConstitutionalChain/get_principles -->

Methodv1.2.13 (latest)●Since v1.0

# get\_principles

Get constitutional principles by name.


```
get_principles(
    cls,
    names: list[str] | None = None,
) -> list[ConstitutionalPrinciple]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `names` | `list[str] | None` | Default:`None`  List of names of constitutional principles to retrieve. If `None` (Default), all principles are returned. |


