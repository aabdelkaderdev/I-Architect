<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/query_constructor/parser/QueryTransformer -->

Classv1.2.13 (latest)●Since v1.0

# QueryTransformer

Transform a query string into an intermediate representation.


```
QueryTransformer(
  self,
  *args: Any = (),
  allowed_comparators: Sequence[Comparator] | None = None,
  allowed_operators: Sequence[Operator] | None = None,
  allowed_attributes: Sequence[str] | None = None,
  **kwargs: Any = {}
)
```

## Bases

`Transformer`

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `*args` | `Any` | Default:`()`  Positional arguments. |
| `allowed_comparators` | `Sequence[Comparator] | None` | Default:`None`  Optional sequence of allowed comparators. |
| `allowed_operators` | `Sequence[Operator] | None` | Default:`None`  Optional sequence of allowed operators. |
| `allowed_attributes` | `Sequence[str] | None` | Default:`None`  Optional sequence of allowed attributes for comparators. |
| `**kwargs` | `Any` | Default:`{}`  Additional keyword arguments. |

## Constructors

constructor

\_\_init\_\_

| Name | Type |
| --- | --- |
| allowed\_comparators | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[Comparator](/python/langchain-core/structured_query/Comparator)] | None |
| allowed\_operators | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[Operator](/python/langchain-core/structured_query/Operator)] | None |
| allowed\_attributes | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None |

## Attributes

[attribute

allowed\_comparators: allowed\_comparators](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/allowed_comparators)[attribute

allowed\_operators: allowed\_operators](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/allowed_operators)[attribute

allowed\_attributes: allowed\_attributes](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/allowed_attributes)

## Methods

[method

program

Transform the items into a tuple.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/program)[method

func\_call

Transform a function name and args into a FilterDirective.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/func_call)[method

args

Transforms items into a tuple.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/args)[method

false

Returns false.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/false)[method

true

Returns true.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/true)[method

list

Transforms an item into a list.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/list)[method

int

Transforms an item into an int.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/int)[method

float

Transforms an item into a float.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/float)[method

date

Transforms an item into a ISO8601Date object.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/date)[method

datetime

Transforms an item into a ISO8601DateTime object.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/datetime)[method

string

Transforms an item into a string.

Removes escaped quotes.](/python/langchain-classic/chains/query_constructor/parser/QueryTransformer/string)


