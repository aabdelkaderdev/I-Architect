<!-- Source: https://reference.langchain.com/python/langchain-classic/output_parsers/format_instructions/PANDAS_DATAFRAME_FORMAT_INSTRUCTIONS -->

Attributev1.2.13 (latest)●Since v1.0

# PANDAS\_DATAFRAME\_FORMAT\_INSTRUCTIONS


```
PANDAS_DATAFRAME_FORMAT_INSTRUCTIONS = 'The output should be formatted as a string as the operation, followed by a colon, followed by the column or row to be queried on, followed by optional array parameters.\n1. The column names are limited to the possible columns below.\n2. Arrays must either be a comma-separated list of numbers formatted as [1,3,5], or it must be in range of numbers formatted as [0..4].\n3. Remember that arrays are optional and not necessarily required.\n4. If the column is not in the possible columns or the operation is not a valid Pandas DataFrame operation, return why it is invalid as a sentence starting with either "Invalid column" or "Invalid operation".\n\nAs an example, for the formats:\n1. String "column:num_legs" is a well-formatted instance which gets the column num_legs, where num_legs is a possible column.\n2. String "row:1" is a well-formatted instance which gets row 1.\n3. String "column:num_legs[1,2]" is a well-formatted instance which gets the column num_legs for rows 1 and 2, where num_legs is a possible column.\n4. String "row:1[num_legs]" is a well-formatted instance which gets row 1, but for just column num_legs, where num_legs is a possible column.\n5. String "mean:num_legs[1..3]" is a well-formatted instance which takes the mean of num_legs from rows 1 to 3, where num_legs is a possible column and mean is a valid Pandas DataFrame operation.\n6. String "do_something:num_legs" is a badly-formatted instance, where do_something is not a valid Pandas DataFrame operation.\n7. String "mean:invalid_col" is a badly-formatted instance, where invalid_col is not a possible column.\n\nHere are the possible columns:\n```\n{columns}\n```\n'
```


