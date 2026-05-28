# Proposal: Data Ingestion & Requirement Filtering

## What
Implement Phase 1: Data Ingestion & Requirement Filtering pipeline, the first module in the I-Architect system. This pipeline accepts various input formats (PDF, DOCX, TXT, JSON), normalises their contents into a flat requirement dictionary, and uses an optional LLM-based agent to filter out noise, outputting a validated requirement set.

The pipeline is implemented as a standalone LangGraph `StateGraph` (compiled to a `Pregel` instance). State is defined using `TypedDict`. The LLM instance (initialised via `init_chat_model` from `langchain.chat_models`, returning a `BaseChatModel`-compatible instance) is passed to nodes through LangGraph's `context_schema` / `Runtime` mechanism — never through state channels — keeping state fully serialisable.

## Why
This phase defines the foundational shared contracts and boundaries necessary for downstream modules (like ARLO) to operate independently. It establishes the input expectations, the standard requirement format (`dict[str, str]`), and the exception taxonomy. By processing raw formats into a predictable structure, it simplifies downstream ingestion.
