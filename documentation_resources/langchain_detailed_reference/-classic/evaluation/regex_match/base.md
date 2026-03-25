<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/regex_match/base -->

Modulev1.2.13 (latest)●Since v1.0

# base

## Classes

[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

RegexMatchStringEvaluator

Compute a regex match between the prediction and the reference.

## Examples:

> > > evaluator = RegexMatchStringEvaluator(flags=re.IGNORECASE)
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^mindy.\*cto$",
> > > ) # This will return {'score': 1.0} due to the IGNORECASE flag

> > > evaluator = RegexMatchStringEvaluator()
> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$",
> > > ) # This will return {'score': 0.0}

> > > evaluator.evaluate\_strings(
> > > prediction="Mindy is the CTO",
> > > reference="^Mike.\*CEO$|^Mindy.\*CTO$",
> > > ) # This will return {'score': 1.0} as the prediction matches the second pattern in the union](/python/langchain-classic/evaluation/regex_match/base/RegexMatchStringEvaluator)


