<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/graph/node_data_json -->

Functionv1.2.21 (latest)●Since v0.1

# node\_data\_json

Convert the data of a node to a JSON-serializable format.


```
node_data_json(
  node: Node,
  *,
  with_schemas: bool = False
) -> dict[str, str | dict[str, Any]]
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `node`\* | `Node` | The `Node` to convert. |
| `with_schemas` | `bool` | Default:`False`  Whether to include the schema of the data if it is a Pydantic model. |


