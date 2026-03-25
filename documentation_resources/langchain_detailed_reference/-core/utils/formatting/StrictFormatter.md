<!-- Source: https://reference.langchain.com/python/langchain-core/utils/formatting/StrictFormatter -->

Classv1.2.21 (latest)●Since v0.1

# StrictFormatter

A string formatter that enforces keyword-only argument substitution.

This formatter extends Python's built-in `string.Formatter` to provide stricter
validation for prompt template formatting. It ensures that all variable
substitutions use keyword arguments rather than positional arguments, which improves
clarity and reduces errors when formatting prompt templates.


```
StrictFormatter()
```

## Bases

`Formatter`

**Example:**

> > > fmt = StrictFormatter()
> > > fmt.format("Hello, {name}!", name="World")
> > > 'Hello, World!'
> > > fmt.format("Hello, {}!", "World") # Raises ValueError

## Methods

[method

vformat

Format a string using only keyword arguments.

Overrides the base `vformat` to reject positional arguments, ensuring all
substitutions are explicit and named.](/python/langchain-core/utils/formatting/StrictFormatter/vformat)[method

validate\_input\_variables

Validate that input variables match the placeholders in a format string.

Checks that the provided input variables can be used to format the given string
without missing or extra keys. This is useful for validating prompt templates
before runtime.](/python/langchain-core/utils/formatting/StrictFormatter/validate_input_variables)


