<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils/NonLocals -->

Classv1.2.21 (latest)●Since v0.1

# NonLocals

Get nonlocal variables accessed.


```
NonLocals(
    self,
)
```

## Bases

`ast.NodeVisitor`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-core/runnables/utils/NonLocals/__init__)

## Attributes

[attribute

loads: set[str]](/python/langchain-core/runnables/utils/NonLocals/loads)[attribute

stores: set[str]](/python/langchain-core/runnables/utils/NonLocals/stores)

## Methods

[method

visit\_Name

Visit a name node.](/python/langchain-core/runnables/utils/NonLocals/visit_Name)[method

visit\_Attribute

Visit an attribute node.](/python/langchain-core/runnables/utils/NonLocals/visit_Attribute)


