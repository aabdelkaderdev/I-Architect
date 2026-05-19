# Implementation Plan: ARLO RAA Compatibility Patch

**Branch**: `002-raa-subgraph` | **Date**: 2026-05-19 | **Spec**: `specs/002-raa-subgraph/spec.md`

**Input**: Feature specification from `specs/002-raa-subgraph/spec.md`

## Summary

Patch ARLO's compatibility boundary for the planned RAA stage by exposing full `non_asr` dictionaries and `condition_groups` through `ARLOOutput`, persisting ASR condition embeddings to project-local SQLite storage at `embeddings/asr_embeddings.db`, and keeping embedding vectors out of downstream LangGraph output state.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: LangGraph 1.2.0, LangChain 1.3.0, FastEmbed 0.8.0, Pydantic 2.13.0, scikit-learn 1.8.0

**Storage**: SQLite database at `embeddings/asr_embeddings.db` for ASR embeddings; `embeddings/` is ignored runtime storage

**Testing**: Python syntax validation and local functional checks against ARLO nodes; pytest is available as an optional dev dependency

**Target Platform**: Local Python runtime on Linux

**Project Type**: Python LangGraph subgraph package

**Performance Goals**: Avoid passing 1024-dimensional embedding vectors through downstream output state or checkpointed parent graph channels

**Constraints**: Scope is restricted to `RAA_Plan.md` Sections 1 and 1B; existing ARLO internal clustering must continue to use the in-memory `embeddings` state channel

**Scale/Scope**: Requirements sets may contain hundreds of requirements; embedding persistence must be keyed by requirement ID and tolerate repeated runs

## Constitution Check

No constitution violations identified for this compatibility patch. The change is limited to existing Python modules, project-local runtime storage, and Spec Kit feature metadata.

## Project Structure

### Documentation (this feature)

```text
specs/002-raa-subgraph/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code (repository root)

```text
arlo/
├── state/
│   └── schemas.py
├── nodes/
│   ├── parsing.py
│   └── embedding.py
├── graphs/
│   ├── core.py
│   ├── influential.py
│   └── varying.py
└── pipeline_wrapper.py

embeddings/
└── asr_embeddings.db

.gitignore
```

**Structure Decision**: Keep the patch inside the existing ARLO package. Use `embeddings/` as shared project-root runtime storage for ARLO and future RAA code.

## Implementation Details

### ARLO Output Compatibility

- Update `ARLOOutput.non_asr` and `ARLOState.non_asr` to `list[dict]`.
- Keep `ARLOOutput.condition_groups` as `list[dict]`.
- Change parsing so non-ASRs retain the same parsed dictionary shape as ASRs.
- Preserve wrapper forwarding without conversion.

### ASR Embedding Persistence

- Keep FastEmbed model name `mixedbread-ai/mxbai-embed-large-v1`.
- Continue returning `{"embeddings": embeddings}` for internal ARLO clustering.
- Add SQLite persistence as a side effect in `arlo/nodes/embedding.py`.
- Use project-root path `embeddings/asr_embeddings.db`.
- Store records keyed by requirement ID to avoid duplicates across reruns.

### Runtime Storage

- `embeddings/` is a runtime directory shared by ARLO and RAA.
- `embeddings/` must remain listed in `.gitignore`.
- SQLite database files under `embeddings/` are not source artifacts.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
