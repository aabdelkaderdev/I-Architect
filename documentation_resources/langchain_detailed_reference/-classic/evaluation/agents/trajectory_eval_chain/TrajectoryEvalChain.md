<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain -->

Classv1.2.13 (latest)●Since v1.0

# TrajectoryEvalChain


```
TrajectoryEvalChain()
```

## Bases

`AgentTrajectoryEvaluator``LLMEvalChain`

## Attributes

## Methods

## Inherited from[AgentTrajectoryEvaluator](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator)

### Attributes

[Arequires\_input: bool

—

Whether this evaluator requires an input string.](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator/requires_input)

### Methods

[Mevaluate\_agent\_trajectory

—

Evaluate a trajectory.](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator/evaluate_agent_trajectory)[Maevaluate\_agent\_trajectory

—

Asynchronously evaluate a trajectory.](/python/langchain-classic/evaluation/schema/AgentTrajectoryEvaluator/aevaluate_agent_trajectory)



## Inherited from[Chain](/python/langchain-classic/chains/base/Chain)

### Attributes

[Amemory: BaseMemory | None

—

Optional memory object.](/python/langchain-classic/chains/base/Chain/memory)[Acallbacks: Callbacks

—

Optional list of callback handlers (or callback manager).](/python/langchain-classic/chains/base/Chain/callbacks)[Averbose: bool

—

Whether or not run in verbose mode. In verbose mode, some intermediate logs](/python/langchain-classic/chains/base/Chain/verbose)[Atags: list[str] | None

—

Optional list of tags associated with the chain.](/python/langchain-classic/chains/base/Chain/tags)[Ametadata: builtins.dict[str, Any] | None

—

Optional metadata associated with the chain.](/python/langchain-classic/chains/base/Chain/metadata)[Acallback\_manager: BaseCallbackManager | None

—

[DEPRECATED] Use `callbacks` instead.](/python/langchain-classic/chains/base/Chain/callback_manager)

### Methods

[Mget\_input\_schema](/python/langchain-classic/chains/base/Chain/get_input_schema)[Mget\_output\_schema](/python/langchain-classic/chains/base/Chain/get_output_schema)[Minvoke](/python/langchain-classic/chains/base/Chain/invoke)[Mainvoke](/python/langchain-classic/chains/base/Chain/ainvoke)[Mraise\_callback\_manager\_deprecation

—

Raise deprecation warning if callback\_manager is used.](/python/langchain-classic/chains/base/Chain/raise_callback_manager_deprecation)[M](/python/langchain-classic/chains/base/Chain/set_verbose)

## Inherited from[RunnableSerializable](/python/langchain-core/runnables/base/RunnableSerializable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/RunnableSerializable/name)

### Methods

[Mto\_json](/python/langchain-core/runnables/base/RunnableSerializable/to_json)[Mconfigurable\_fields](/python/langchain-core/runnables/base/RunnableSerializable/configurable_fields)[Mconfigurable\_alternatives](/python/langchain-core/runnables/base/RunnableSerializable/configurable_alternatives)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)(langchain\_core)

### Attributes

[Alc\_secrets](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes](/python/langchain-core/load/serializable/Serializable/lc_attributes)

### Methods

[Mis\_lc\_serializable](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)

## Inherited from[Runnable](/python/langchain-core/runnables/base/Runnable)(langchain\_core)

### Attributes

[Aname](/python/langchain-core/runnables/base/Runnable/name)[AInputType](/python/langchain-core/runnables/base/Runnable/InputType)[AOutputType](/python/langchain-core/runnables/base/Runnable/OutputType)[Ainput\_schema](/python/langchain-core/runnables/base/Runnable/input_schema)[Aoutput\_schema](/python/langchain-core/runnables/base/Runnable/output_schema)[Aconfig\_specs](/python/langchain-core/runnables/base/Runnable/config_specs)

### Methods

[Mget\_name](/python/langchain-core/runnables/base/Runnable/get_name)[Mget\_input\_schema](/python/langchain-core/runnables/base/Runnable/get_input_schema)[Mget\_input\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_input_jsonschema)[Mget\_output\_schema](/python/langchain-core/runnables/base/Runnable/get_output_schema)[Mget\_output\_jsonschema](/python/langchain-core/runnables/base/Runnable/get_output_jsonschema)[Mconfig\_schema](/python/langchain-core/runnables/base/Runnable/config_schema)

[attribute

agent\_tools: list[BaseTool] | None

A list of tools available to the agent.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/agent_tools)

[attribute

eval\_chain: LLMChain

The language model chain used for evaluation.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/eval_chain)

[attribute

output\_parser: TrajectoryOutputParser

The output parser used to parse the output.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/output_parser)

[attribute

return\_reasoning: bool

DEPRECATED. Reasoning always returned.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/return_reasoning)

[attribute

model\_config](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/model_config)

[attribute

requires\_reference: bool

Whether this evaluator requires a reference label.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/requires_reference)

[attribute

input\_keys: list[str]

Get the input keys for the chain.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/input_keys)

[attribute

output\_keys: list[str]

Get the output keys for the chain.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/output_keys)

[method

get\_agent\_trajectory

Get the agent trajectory as a formatted string.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/get_agent_trajectory)

[method

from\_llm

Create a TrajectoryEvalChain object from a language model chain.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/from_llm)

[method

prep\_inputs

Validate and prep inputs.](/python/langchain-classic/evaluation/agents/trajectory_eval_chain/TrajectoryEvalChain/prep_inputs)

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
```

set\_verbose

—

Set the chain verbosity.

[Macall

—

Asynchronously execute the chain.](/python/langchain-classic/chains/base/Chain/acall)

[Mprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/prep_outputs)

[Maprep\_outputs

—

Validate and prepare chain outputs, and save info about this run to memory.](/python/langchain-classic/chains/base/Chain/aprep_outputs)

[Maprep\_inputs

—

Prepare chain inputs, including adding inputs from memory.](/python/langchain-classic/chains/base/Chain/aprep_inputs)

[Mrun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/run)

[Marun

—

Convenience method for executing chain.](/python/langchain-classic/chains/base/Chain/arun)

[Mdict

—

Dictionary representation of chain.](/python/langchain-classic/chains/base/Chain/dict)

[Msave

—

Save the chain.](/python/langchain-classic/chains/base/Chain/save)

[Mapply

—

Call the chain on all inputs in the list.](/python/langchain-classic/chains/base/Chain/apply)

M

get\_config\_jsonschema

[Mget\_graph](/python/langchain-core/runnables/base/Runnable/get_graph)

[Mget\_prompts](/python/langchain-core/runnables/base/Runnable/get_prompts)

[Mpipe](/python/langchain-core/runnables/base/Runnable/pipe)

[Mpick](/python/langchain-core/runnables/base/Runnable/pick)

[Massign](/python/langchain-core/runnables/base/Runnable/assign)

[Minvoke](/python/langchain-core/runnables/base/Runnable/invoke)

[Mainvoke](/python/langchain-core/runnables/base/Runnable/ainvoke)

[Mbatch](/python/langchain-core/runnables/base/Runnable/batch)

[Mbatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/batch_as_completed)

[Mabatch](/python/langchain-core/runnables/base/Runnable/abatch)

[Mabatch\_as\_completed](/python/langchain-core/runnables/base/Runnable/abatch_as_completed)

[Mstream](/python/langchain-core/runnables/base/Runnable/stream)

[Mastream](/python/langchain-core/runnables/base/Runnable/astream)

[Mastream\_log](/python/langchain-core/runnables/base/Runnable/astream_log)

[Mastream\_events](/python/langchain-core/runnables/base/Runnable/astream_events)

[Mtransform](/python/langchain-core/runnables/base/Runnable/transform)

[Matransform](/python/langchain-core/runnables/base/Runnable/atransform)

[Mbind](/python/langchain-core/runnables/base/Runnable/bind)

[Mwith\_config](/python/langchain-core/runnables/base/Runnable/with_config)

[Mwith\_listeners](/python/langchain-core/runnables/base/Runnable/with_listeners)

[Mwith\_alisteners](/python/langchain-core/runnables/base/Runnable/with_alisteners)

[Mwith\_types](/python/langchain-core/runnables/base/Runnable/with_types)

[Mwith\_retry](/python/langchain-core/runnables/base/Runnable/with_retry)

[Mmap](/python/langchain-core/runnables/base/Runnable/map)

[Mwith\_fallbacks](/python/langchain-core/runnables/base/Runnable/with_fallbacks)

[Mas\_tool](/python/langchain-core/runnables/base/Runnable/as_tool)