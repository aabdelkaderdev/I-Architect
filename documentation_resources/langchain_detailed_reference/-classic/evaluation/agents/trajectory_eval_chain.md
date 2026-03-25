<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_chain -->

Modulev1.2.13 (latest)●Since v1.0

# trajectory\_eval\_chain

A chain for evaluating ReAct style agents.

This chain is used to evaluate ReAct style agents by reasoning about
the sequence of actions taken and their outcomes. It uses a language model
chain (LLMChain) to generate the reasoning and scores.

## Attributes

[attribute

EVAL\_CHAT\_PROMPT](/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/EVAL_CHAT_PROMPT)[attribute

TOOL\_FREE\_EVAL\_CHAT\_PROMPT](/python/langchain-classic/evaluation/agents/trajectory_eval_prompt/TOOL_FREE_EVAL_CHAT_PROMPT)

## Classes

[class

AgentTrajectoryEvaluator

Interface for evaluating agent trajectories.](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator)[class

LLMEvalChain

A base class for evaluators that use an LLM.](/python/langchain-classic/evaluation/schema/LLMEvalChain)[class

TrajectoryEval

A named tuple containing the score and reasoning for a trajectory.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEval)[class

TrajectoryOutputParser

Trajectory output parser.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryOutputParser)[class

TrajectoryEvalChain

A chain for evaluating ReAct style agents.

This chain is used to evaluate ReAct style agents by reasoning about
the sequence of actions taken and their outcomes.
Based on the paper "ReAct: Synergizing Reasoning and Acting in Language Models"
(<https://arxiv.org/abs/2210.03629>)

Example:

```
from langchain_classic.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_classic.evaluation import TrajectoryEvalChain
from langchain_classic.tools import tool

@tool
def geography_answers(country: str, question: str) -> str:
    """Very helpful answers to geography questions."""
    return f"{country}? IDK - We may never know {question}."

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = initialize_agent(
    tools=[geography_answers],
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    return_intermediate_steps=True,
)

question = "How many dwell in the largest minor region in Argentina?"
response = agent(question)

eval_chain = TrajectoryEvalChain.from_llm(
    llm=model, agent_tools=[geography_answers], return_reasoning=True
)

result = eval_chain.evaluate_agent_trajectory(
    input=question,
    agent_trajectory=response["intermediate_steps"],
    prediction=response["output"],
    reference="Paris",
)
print(result["score"])  # noqa: T201
# 0
```](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain)[deprecatedclass

LLMChain

Chain to run queries against LLMs.

This class is deprecated. See below for an example implementation using
LangChain runnables:

```
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(input_variables=["adjective"], template=prompt_template)
model = OpenAI()
chain = prompt | model | StrOutputParser()

chain.invoke("your adjective here")
```](/python/langchain-classic/chains/llm/LLMChain)


