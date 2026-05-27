## Why

We need to build the core processing loop that orchestrates the entire AGA workflow. This involves creating an agent node that handles diagram generation, error handling, encoding, fetching, and validation. Additionally, we need to wire together all previously created nodes (Server Guard, Input Parsing, Tools) using a LangGraph StateGraph, establishing conditional routing and checkpointing, so we have a fully functional end-to-end architecture diagram generator.

## What Changes

- Create an agent node using `create_agent` (from `langchain.agents`) that generates, encodes, fetches, and validates PlantUML diagrams per task. This replaces the deprecated `create_react_agent` from `langgraph.prebuilt`.
- Implement error handling via agent middleware (`AgentMiddleware` subclass with `wrap_tool_call` and `after_model` hooks) for different failure conditions (e.g., encoding errors, syntax errors, HTTP errors) with a defined maximum retry limit.
- Create an output assembly node to handle completion of the diagram processing queue.
- Implement the LangGraph `StateGraph` in `aga_graph.py` to wire `server_guard`, `input_parsing`, `agent_node`, and `output_assembly` together with conditional edges.
- Configure `SqliteSaver` checkpointer (from `langgraph-checkpoint-sqlite`) to persist state after each completed diagram.
- Ensure the state graph consumes the `AGAState` TypedDict schema and interacts with the predefined tools and prompts.
- Use LangGraph's `Runtime` object for dependency injection (LLM, context) into nodes, replacing the deprecated `config["configurable"]` pattern.

## Capabilities

### New Capabilities
- `agent-loop`: A `create_agent`-based agent (from `langchain.agents`) that loops through generating, encoding, fetching, and validating PlantUML for a given diagram task. Includes self-correction logic via middleware and halt/retry rules.
- `output-assembly`: Processing node that executes when the diagram queue is exhausted, finalizing outputs.
- `agent-graph`: The main LangGraph StateGraph topology, defining nodes, conditional edges, graph traversal logic, and checkpointing strategy using `SqliteSaver` from `langgraph-checkpoint-sqlite`.

### Modified Capabilities
- (None)

## Impact

- Adds new node implementations at `aga/nodes/diagram_generation.py` and `aga/nodes/output_assembly.py`.
- Introduces `aga/graphs/aga_graph.py` and `aga/graphs/__init__.py`.
- Requires `langchain>=1.0` (for `create_agent`, `langchain.agents`, `langchain.tools`) and `langgraph-checkpoint-sqlite` (for `SqliteSaver`).
- Directly impacts the execution path, turning individual capabilities into a complete, executable end-to-end pipeline.
