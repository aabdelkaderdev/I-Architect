<!-- Source: https://reference.langchain.com/python/langchain-classic/smith/evaluation/string_run_evaluator -->

Modulev1.2.13 (latest)●Since v1.0

# string\_run\_evaluator

Run evaluator wrapper for string evaluators.

## Attributes

[attribute

RUN\_KEY: str](/python/langchain-classic/schema/RUN_KEY)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

StringRunMapper

Extract items to evaluate from the run object.](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunMapper)[class

LLMStringRunMapper

Extract items to evaluate from the run object.](/python/langchain-classic/smith/evaluation/string_run_evaluator/LLMStringRunMapper)[class

ChainStringRunMapper

Extract items to evaluate from the run object from a chain.](/python/langchain-classic/smith/evaluation/string_run_evaluator/ChainStringRunMapper)[class

ToolStringRunMapper

Map an input to the tool.](/python/langchain-classic/smith/evaluation/string_run_evaluator/ToolStringRunMapper)[class

StringExampleMapper

Map an example, or row in the dataset, to the inputs of an evaluation.](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringExampleMapper)[class

StringRunEvaluatorChain

Evaluate Run and optional examples.](/python/langchain-classic/smith/evaluation/string_run_evaluator/StringRunEvaluatorChain)


