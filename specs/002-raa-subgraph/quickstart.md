# Quickstart Guide: RAA State Contracts

This guide shows how to import and use the RAA state dataclasses, state channels, and custom reducers.

## 1. Importing Dataclasses

State types and structural models are located in `raa.state.types`:

```python
from raa.state.types import (
    ArchModel,
    ArchFragment,
    ArchSystem,
    ArchContainer,
    ArchComponent,
    ArchRelationship,
    OpenQuestion
)

# Instantiate a C4 System
payment_system = ArchSystem(
    id="payment_gateway",
    label="Payment Gateway System",
    description="Processes incoming payments and transactions",
    requirement_ids=[101, 102],
    source_fragment="raa_a",
    confidence=0.9,
    context_relationships=[],
    containers=[]
)
```

## 2. Using the State Channels TypedDict

The central state TypedDict is defined in `raa.state.channels`:

```python
from raa.state.channels import RAAState

# Initializing an empty state dict matching RAAState
initial_state: RAAState = {
    "batch_queue": [],
    "batch_cursor": 0,
    "batch_outputs": {},
    "best_batch_output": {},
    "running_arch_model": ArchModel(
        systems=[],
        persons=[],
        external_systems=[],
        patterns=[],
        open_questions=[]
    ),
    "open_questions": [],
    "bridge_requirements": {},
    "incoherent_batches": [],
    "embeddings_ready": False
}
```

## 3. Merging Outputs via Custom Reducers

Multi-writer channels rely on reducers imported from `raa.state.reducers` (configured on the state TypedDict):

```python
from raa.state.reducers import merge_batch_outputs

# Parallel subgraphs execute and emit their outputs for batch 0
output_subgraph_a = {0: [fragment_a]}
output_subgraph_b = {0: [fragment_b]}

# LangGraph invokes the reducer to merge the parallel writes:
merged_outputs = merge_batch_outputs(output_subgraph_a, output_subgraph_b)
# merged_outputs is now {0: [fragment_a, fragment_b]}
```
