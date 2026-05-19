# Cross-Batch Coherence Injection Contracts

The serialization helper must output sorted C4 elements by ID.
The output representation must represent nesting: Systems -> Containers -> Components.
The constraints payload must be prefixed exactly with:
`The following components and relationships are already part of the architecture model. You must be consistent with them. Do not rename, restructure, or contradict any listed entity or relationship.`
The generated text must be injected into the prompt variables of all strategy nodes.
