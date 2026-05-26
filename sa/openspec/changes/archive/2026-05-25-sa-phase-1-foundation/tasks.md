## 1. Setup & Foundations

- [x] 1.1 Create `sa/` package structure and empty `__init__.py` files
- [x] 1.2 Define `ScoringReport`, `AxisScore`, and `Penalty` schemas in `sa/state/models.py`
- [x] 1.3 Define LangGraph State typed dictionary in `sa/state/schemas.py`
- [x] 1.4 Create `sa/runner.py` with empty graph compilation function

## 2. Node 1: Data Preparation

- [x] 2.1 Implement utility for traversing flat entity list and reconstructing C4 hierarchy
- [x] 2.2 Implement utility for extracting `traceability_matrix`
- [x] 2.3 Implement utility for extracting flattened technology list and patterns
- [x] 2.4 Create `sa/nodes/preparation.py` to aggregate utils and update state
- [x] 2.5 Add tests for `sa/nodes/preparation.py`

## 3. Mock Nodes (Nodes 2, 3, 4)

- [x] 3.1 Create `sa/nodes/axis_functional.py` with mock Node 2 function
- [x] 3.2 Create `sa/nodes/axis_asr.py` with mock Node 3 function
- [x] 3.3 Create `sa/nodes/axis_saam.py` with mock Node 4 function

## 4. Node 5: Report Generation

- [x] 4.1 Implement deterministic grade calculation logic in `sa/nodes/report.py`
- [x] 4.2 Add deterministic JSON reporting and markdown stub generation in `sa/nodes/report.py`
- [x] 4.3 Add tests for grade calculation logic

## 5. Graph Wiring & Execution

- [x] 5.1 Update `sa/graphs/core.py` to wire Nodes 1-5 sequentially using `builder.add_edge()` (from `START` to `END`)
- [x] 5.2 Update `sa/runner.py` to compile the graph (`builder.compile()`) and invoke it end-to-end
- [x] 5.3 Write end-to-end test verifying a zero-score report is produced
