<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/parser/GRAMMAR -->

Attributev1.2.13 (latest)●Since v1.0

# GRAMMAR


```
GRAMMAR = '\n    ?program: func_call\n    ?expr: func_call\n        | value\n\n    func_call: CNAME "(
  " [args] ")"\n\n    ?value: SIGNED_INT -> int\n        | SIGNED_FLOAT -> float\n        | DATE -> date\n        | DATETIME -> datetime\n        | list\n        | string\n        | ("false" | "False" | "FALSE") -> false\n        | ("true" | "True" | "TRUE") -> true\n\n    args: expr ("," expr)*\n    DATE.2: /["\']?(\\d{4}-[01]\\d-[0-3]\\d
)["\']?/\n    DATETIME.2: /["\']?\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d:[0-5]\\d[Zz]?["\']?/\n    string: /\'[^\']*\'/ | ESCAPED_STRING\n    list: "[" [args] "]"\n\n    %import common.CNAME\n    %import common.ESCAPED_STRING\n    %import common.SIGNED_FLOAT\n    %import common.SIGNED_INT\n    %import common.WS\n    %ignore WS\n'
```


