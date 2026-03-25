<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/scoring -->

Modulev1.2.13 (latest)●Since v1.0

# scoring

Scoring evaluators.

This module contains evaluators for scoring on a 1-10 the output of models,
be they LLMs, Chains, or otherwise. This can be based on a variety of
criteria and or a reference answer.

**Example:**

> > > from langchain\_openai import ChatOpenAI
> > > from langchain\_classic.evaluation.scoring import ScoreStringEvalChain
> > > model = ChatOpenAI(temperature=0, model\_name="gpt-4")
> > > chain = ScoreStringEvalChain.from\_llm(llm=model)
> > > result = chain.evaluate\_strings(
> > > ... input="What is the chemical formula for water?",
> > > ... prediction="H2O",
> > > ... reference="The chemical formula for water is H2O.",
> > > ... )
> > > print(result)

# {

# "score": 8,

# "comment": "The response accurately states "

# "that the chemical formula for water is H2O."

# "However, it does not provide an explanation of what the formula means."

# }

## Classes

[class

LabeledScoreStringEvalChain

A chain for scoring the output of a model on a scale of 1-10.](/python/langchain-classic/evaluation/scoring/eval_chain/LabeledScoreStringEvalChain)[class

ScoreStringEvalChain

A chain for scoring on a scale of 1-10 the output of a model.](/python/langchain-classic/evaluation/scoring/eval_chain/ScoreStringEvalChain)

## Modules

[module

eval\_chain

Base classes for scoring the output of a model on a scale of 1-10.](/python/langchain-classic/evaluation/scoring/eval_chain)[module

prompt

Prompts for scoring the outputs of a models for a given question.

This prompt is used to score the responses and evaluate how it follows the instructions
and answers the question. The prompt is based on the paper from
Zheng, et. al. <https://arxiv.org/abs/2306.05685>](/python/langchain-classic/evaluation/scoring/prompt)


