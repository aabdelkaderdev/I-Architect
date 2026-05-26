## Why

The Scoring Agent (SA) needs to evaluate the architecture model against functional and ASR requirements. Building all 5 nodes with their LLM integrations at once violates the OpenSpec task constraints and is risky. Phase 1 establishes a "Walking Skeleton" of the pipeline, providing the LangGraph foundation, data ingestion, and deterministic reporting mechanics. This unblocks subsequent sequential work on the complex scoring nodes.

## What Changes

- Create the LangGraph StateGraph definition and wiring for a 5-node sequential pipeline.
- Implement state schemas (`schemas.py`, `models.py`) for the entire scoring process.
- Implement Node 1 (Data Prep) to traverse the architecture model, build the traceability matrix, and extract orphaned requirements.
- Implement the deterministic portion of Node 5 (Report) to compute grades and output the `ScoringReport` JSON structure.
- Add mock passthroughs for Nodes 2, 3, and 4 (returning 0 scores) and stub the LLM narrative in Node 5.
- Create an entry point `runner.py` to invoke the graph.

## Capabilities

### New Capabilities
- `pipeline-foundation`: The core LangGraph state graph setup, schemas, and runner.
- `data-preparation`: Parsing of the C4 architecture model, relationship mapping, and traceability matrix construction.
- `deterministic-reporting`: The math to compute the final letter grade and export the `scoring_report.json`.

### Modified Capabilities

## Impact

- Introduces the new `sa/` package structure.
- Establishes the `sa_graph` invocation contract expected by the (future) orchestrator.
- Output files `scoring_report.json` and a stubbed `scoring_report.md` will be generated in the specified output path.
