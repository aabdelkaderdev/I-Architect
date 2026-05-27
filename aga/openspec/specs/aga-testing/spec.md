## ADDED Requirements

### Requirement: AGA Module Validation Scaffolding
The project SHALL include test scaffolding to validate the end-to-end capabilities, logic functions, and output schemas of the AGA module.

#### Scenario: Unit tests pass
- **WHEN** the test suite executes unit tests for OS detection, PlantUML encoding, error classification, and queue derivation
- **THEN** all tests succeed and properly enforce expected logic.

#### Scenario: Integration test with test fixture
- **WHEN** the end-to-end integration test runs using `arch_model_test_result-1.json`
- **THEN** the agent generates all derivable diagrams successfully, producing valid PNG and .puml files.

#### Scenario: Syntax error injection resilience
- **WHEN** a syntax error is injected during generation in tests
- **THEN** the agent correctly corrects and renders it on a retry.
