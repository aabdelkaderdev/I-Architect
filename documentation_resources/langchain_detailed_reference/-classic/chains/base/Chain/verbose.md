<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/base/Chain/verbose -->

Attributev1.2.13 (latest)●Since v1.0

# verbose

Whether or not run in verbose mode. In verbose mode, some intermediate logs
will be printed to the console. Defaults to the global `verbose` value,
accessible via `langchain.globals.get_verbose()`.


```
verbose: bool = Field(default_factory=_get_verbosity)
```


