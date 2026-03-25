<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/comparison -->

Modulev1.2.13 (latest)●Since v1.0

# comparison

Comparison evaluators.

This module contains evaluators for comparing the output of two models,
be they LLMs, Chains, or otherwise. This can be used for scoring
preferences, measuring similarity / semantic equivalence between outputs,
or any other comparison task.

**Example:**

> > > from langchain\_openai import ChatOpenAI
> > > from langchain\_classic.evaluation.comparison import PairwiseStringEvalChain
> > > llm = ChatOpenAI(temperature=0)
> > > chain = PairwiseStringEvalChain.from\_llm(llm=llm)
> > > result = chain.evaluate\_string\_pairs(
> > > ... input = "What is the chemical formula for water?",
> > > ... prediction = "H2O",
> > > ... prediction\_b = (
> > > ... "The chemical formula for water is H2O, which means"
> > > ... " there are two hydrogen atoms and one oxygen atom."
> > > ... reference = "The chemical formula for water is H2O.",
> > > ... )
> > > print(result)

# {

# "value": "B",

# "comment": "Both responses accurately state"

# " that the chemical formula for water is H2O."

# " However, Response B provides additional information"

# . " by explaining what the formula means.\n[[B]]"

# }

## Classes

[class

LabeledPairwiseStringEvalChain

Labeled Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs,
with labeled preferences.](/python/langchain-classic/evaluation/comparison/eval_chain/LabeledPairwiseStringEvalChain)[class

PairwiseStringEvalChain

Pairwise String Evaluation Chain.

A chain for comparing two outputs, such as the outputs
of two models, prompts, or outputs of a single model on similar inputs.](/python/langchain-classic/evaluation/comparison/eval_chain/PairwiseStringEvalChain)

## Modules

[module

eval\_chain

Base classes for comparing the output of two models.](/python/langchain-classic/evaluation/comparison/eval_chain)[module

prompt

Prompts for comparing the outputs of two models for a given question.

This prompt is used to compare two responses and evaluate which one best follows the instructions
and answers the question. The prompt is based on the paper from
Zheng, et. al. <https://arxiv.org/abs/2306.05685>](/python/langchain-classic/evaluation/comparison/prompt)


