<!-- Source: https://reference.langchain.com/python/langchain-core/structured_query/Visitor -->

Classv1.2.21 (latest)●Since v0.1

# Visitor

Defines interface for IR translation using a visitor pattern.


```
Visitor()
```

## Bases

`ABC`

## Attributes

[attribute

allowed\_comparators: Sequence[Comparator] | None

Allowed comparators for the visitor.](/python/langchain-core/structured_query/Visitor/allowed_comparators)[attribute

allowed\_operators: Sequence[Operator] | None

Allowed operators for the visitor.](/python/langchain-core/structured_query/Visitor/allowed_operators)

## Methods

[method

visit\_operation

Translate an Operation.](/python/langchain-core/structured_query/Visitor/visit_operation)[method

visit\_comparison

Translate a Comparison.](/python/langchain-core/structured_query/Visitor/visit_comparison)[method

visit\_structured\_query

Translate a StructuredQuery.](/python/langchain-core/structured_query/Visitor/visit_structured_query)


