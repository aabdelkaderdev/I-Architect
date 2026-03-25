<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/pandas_dataframe/PandasDataFrameOutputParser/parse_array -->

Methodv1.2.13 (latest)●Since v1.0

# parse\_array

Parse the array from the request parameters.


```
parse_array(
  self,
  array: str,
  original_request_params: str
) -> tuple[list[int | str], str]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `array`\* | `str` | The array string to parse. |
| `original_request_params`\* | `str` | The original request parameters string. |


