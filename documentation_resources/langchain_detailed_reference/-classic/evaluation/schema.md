<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/schema -->

Modulev1.2.13 (latest)●Since v1.0

# schema

Interfaces to be implemented by general evaluators.

## Attributes

[attribute

logger](/python/langchain-classic/evaluation/schema/logger)

## Classes

[class

Chain

Abstract base class for creating structured sequences of calls to components.

Chains should be used to encode a sequence of calls to components like
models, document retrievers, other chains, etc., and provide a simple interface
to this sequence.](/python/langchain-classic/chains/base/Chain)[class

EvaluatorType

The types of the evaluators.](/python/langchain-classic/evaluation/schema/EvaluatorType)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

StringEvaluator

String evaluator interface.

Grade, tag, or otherwise evaluate predictions relative to their inputs
and/or reference labels.](/python/langchain-classic/evaluation/schema/StringEvaluator)[class

PairwiseStringEvaluator

Compare the output of two models (or two outputs of the same model).](/python/langchain-classic/evaluation/schema/PairwiseStringEvaluator)[class

AgentTrajectoryEvaluator

Interface for evaluating agent trajectories.](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator)


