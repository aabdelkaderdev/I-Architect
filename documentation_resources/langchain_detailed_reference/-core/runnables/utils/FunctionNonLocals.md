<!-- Source: https://reference.langchain.com/python/langchain-core/runnables/utils/FunctionNonLocals -->

Classv1.2.21 (latest)●Since v0.1

# FunctionNonLocals

Get the nonlocal variables accessed of a function.


```
FunctionNonLocals(
    self,
)
```

## Bases

`ast.NodeVisitor`

## Constructors

[constructor

\_\_init\_\_](/python/langchain-core/runnables/utils/FunctionNonLocals/__init__)

## Attributes

[attribute

nonlocals: set[str]](/python/langchain-core/runnables/utils/FunctionNonLocals/nonlocals)

## Methods

[method

visit\_FunctionDef

Visit a function definition.](/python/langchain-core/runnables/utils/FunctionNonLocals/visit_FunctionDef)[method

visit\_AsyncFunctionDef

Visit an async function definition.](/python/langchain-core/runnables/utils/FunctionNonLocals/visit_AsyncFunctionDef)[method

visit\_Lambda

Visit a lambda function.](/python/langchain-core/runnables/utils/FunctionNonLocals/visit_Lambda)


