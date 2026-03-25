<!-- Source: https://reference.langchain.com/python/langchain-core/tracers/evaluation -->

Modulev1.2.21 (latest)●Since v0.1

# evaluation

A tracer that runs evaluators over completed runs.

## Attributes

[attribute

Run: RunTree](/python/langchain-core/tracers/schemas/Run)[attribute

logger](/python/langchain-core/tracers/evaluation/logger)

## Functions

[function

run\_copy

Copy run, compatible with both Pydantic v1 and v2.](/python/langchain-core/tracers/_compat/run_copy)[function

tracing\_v2\_enabled

Instruct LangChain to log all runs in context to LangSmith.](/python/langchain-core/tracers/context/tracing_v2_enabled)[function

wait\_for\_all\_evaluators

Wait for all tracers to finish.](/python/langchain-core/tracers/evaluation/wait_for_all_evaluators)

## Classes

[class

BaseTracer

Base interface for tracers.](/python/langchain-core/tracers/base/BaseTracer)[class

EvaluatorCallbackHandler

Tracer that runs a run evaluator whenever a run is persisted.](/python/langchain-core/tracers/evaluation/EvaluatorCallbackHandler)

## Modules

[module

langchain\_tracer

A tracer implementation that records to LangChain endpoint.](/python/langchain-core/tracers/langchain)


