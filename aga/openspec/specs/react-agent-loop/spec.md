# react-agent-loop Specification

## Purpose
TBD - created by archiving change phase-5-agent-graph. Update Purpose after archive.
## Requirements
### Requirement: Agent Loop Initialization
The system SHALL initialize an agent using `langchain.agents.create_agent` to process each diagram task, with tools bound via the `tools=` parameter and instructions via the `system_prompt=` parameter.

#### Scenario: Agent loop processes diagram
- **WHEN** the `diagram_loop_entry` transitions to `agent_node`
- **THEN** the system invokes the `create_agent`-based agent to generate, encode, and fetch the PlantUML diagram

### Requirement: Agent Self-Correction via Middleware
The agent SHALL perform self-correction up to a maximum of 5 retries upon failure, managed through a custom `AgentMiddleware` subclass that tracks retry count in state and intercepts tool errors via `wrap_tool_call`.

#### Scenario: Agent encounters syntax error
- **WHEN** the `fetch_plantuml_png` tool returns an error regarding syntax
- **THEN** the middleware intercepts the error via `wrap_tool_call`, increments the retry count, and allows the agent loop to continue with error context

#### Scenario: Agent exhausts retries
- **WHEN** the agent fails 5 times for a single diagram (tracked via middleware `state_schema`)
- **THEN** the middleware's `before_model` hook returns `{"jump_to": "end"}` to halt the agent, and the system records the failure and proceeds to the next diagram in the queue

