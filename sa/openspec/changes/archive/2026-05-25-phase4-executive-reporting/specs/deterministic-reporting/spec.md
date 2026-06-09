## MODIFIED Requirements

### Requirement: JSON Report Output
The system SHALL validate that the provided output directory exists and is writable before exporting the structured `ScoringReport` as a JSON file, raising explicit errors if validation fails. The current `os.makedirs(output_path, exist_ok=True)` in `sa/nodes/report.py` SHALL be replaced with validation-only checks (the orchestrator is responsible for directory creation).

#### Scenario: JSON Export Success
- **WHEN** Node 5 completes execution and the output directory exists and is writable
- **THEN** it writes `scoring_report.json` to the target directory containing the full schema, including `diagram_issues` populated from Node 4

#### Scenario: Output Path Not Found
- **WHEN** the `output_path` directory does not exist
- **THEN** the system raises an explicit `FileNotFoundError` indicating the directory does not exist

#### Scenario: Output Path Not Writable
- **WHEN** the `output_path` directory exists but lacks write permissions
- **THEN** the system raises a `PermissionError` and still returns the valid `ScoringReport` in its state
