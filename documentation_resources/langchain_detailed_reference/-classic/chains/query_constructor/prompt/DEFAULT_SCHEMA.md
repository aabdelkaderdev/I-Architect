<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/prompt/DEFAULT_SCHEMA -->

Attributev1.2.13 (latest)●Since v1.0

# DEFAULT\_SCHEMA


```
DEFAULT_SCHEMA = '<
  < Structured Request Schema >
>\nWhen responding use a markdown code snippet with a JSON object formatted in the following schema:\n\n```json\n{{{{\n    "query": string \\ text string to compare to document contents\n    "filter": string \\ logical condition statement for filtering documents\n}}}}\n```\n\nThe query string should contain only text that is expected to match the contents of documents. Any conditions in the filter should not be mentioned in the query as well.\n\nA logical condition statement is composed of one or more comparison and logical operation statements.\n\nA comparison statement takes the form: `comp(
  attr,
  val)`:\n- `comp` ({allowed_comparators}): comparator\n- `attr` (string):  name of attribute to apply the comparison to\n- `val` (string): is the comparison value\n\nA logical operation statement takes the form `op(statement1,
  statement2,
  ...)`:\n- `op` ({allowed_operators}): logical operator\n- `statement1`, `statement2`, ... (comparison statements or logical operation statements
): one or more statements to apply the operation to\n\nMake sure that you only use the comparators and logical operators listed above and no others.\nMake sure that filters only refer to attributes that exist in the data source.\nMake sure that filters only use the attributed names with its function names if there are functions applied on them.\nMake sure that filters only use format `YYYY-MM-DD` when handling date data typed values.\nMake sure that filters take into account the descriptions of attributes and only make comparisons that are feasible given the type of data being stored.\nMake sure that filters are only used as needed. If there are no filters that should be applied return "NO_FILTER" for the filter value.'
```


