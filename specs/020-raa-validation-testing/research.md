# Research: RAA Validation and Testing Strategy

## Decision: Testing Framework
**Decision**: Use `pytest` for all unit, integration, and functional tests.
**Rationale**: It is the existing standard for the project, supports powerful fixture injection for managing temporary SQLite databases, and has great plugin support for asyncio testing (`pytest-asyncio`) which LangGraph requires.
**Alternatives considered**: Standard library `unittest` (too verbose, poor fixture support).

## Decision: LLM Mocking Strategy
**Decision**: Implement a `FakeChatModel` or `MockLLM` class that conforms to the `BaseChatModel` interface required by LangChain/LangGraph, injecting deterministic responses based on input prompts.
**Rationale**: The pipeline requires four injected LLM instances. Real LLM calls would introduce latency, cost, and non-determinism, violating the < 2 minutes performance goal. A controlled mock allows tests to focus on the pipeline logic (merging, scoring, deduplication).
**Alternatives considered**: Network recording libraries like VCR.py (overkill, creates large binary cassettes, doesn't handle dynamic prompt variations well).

## Decision: SQLite Database Isolation
**Decision**: Use `pytest`'s built-in `tmp_path` fixture to dynamically create separate `embeddings/` directories with blank `asr_embeddings.db` and `non_asr_embeddings.db` for each test.
**Rationale**: Ensures tests run in perfect isolation, preventing parallel execution conflicts and state leaking.
**Alternatives considered**: In-memory SQLite (`:memory:`) (Not viable since FastEmbed or node tools require a concrete filesystem path to open WAL mode databases across different node contexts).
