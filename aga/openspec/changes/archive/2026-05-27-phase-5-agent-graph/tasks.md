## 1. Node Implementations

- [x] 1.1 Create `aga/nodes/diagram_generation.py` to house the agent logic
- [x] 1.2 Implement agent loop using `create_agent` from `langchain.agents`, binding tools via `tools=` and instructions via `system_prompt=`
- [x] 1.3 Implement a custom `AgentMiddleware` subclass with `wrap_tool_call` (error interception) and `before_model` (retry limit enforcement with `{"jump_to": "end"}`)
- [x] 1.4 Create `aga/nodes/output_assembly.py` to handle queue exhaustion and final state formatting

## 2. Graph Wiring

- [x] 2.1 Create `aga/graphs/__init__.py` and `aga/graphs/aga_graph.py`
- [x] 2.2 Define `StateGraph` using `AGAState` TypedDict schema (Pydantic not supported by `create_agent`)
- [x] 2.3 Add `server_guard`, `input_parsing`, `agent_node`, and `output_assembly` nodes to the graph via `add_node`
- [x] 2.4 Implement conditional edges via `add_conditional_edges` to route diagrams sequentially, and branch on completion or failure
- [x] 2.5 Configure `SqliteSaver` from `langgraph-checkpoint-sqlite` and compile the graph with `graph.compile(checkpointer=checkpointer)`
- [x] 2.6 Define a `Context` dataclass and ensure nodes accept `runtime: Runtime[Context]` for LLM/dependency injection

## 3. Testing

- [x] 3.1 Write test verifying end-to-end processing with `arch_model_test_result-1.json` fixture
- [x] 3.2 Write test simulating a syntax error and verifying the agent's middleware-based self-correction loop
- [x] 3.3 Write test simulating a 503 Server Unavailable response and verifying immediate graph halting
