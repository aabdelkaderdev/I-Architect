## ADDED Requirements

### Requirement: Validate standard JSON structure
The system SHALL validate JSON files against the standard requirement schema (must be a dict root, all keys must be strings, all values must be strings, no nested structures).

#### Scenario: Compliant JSON uploaded
- **WHEN** a valid JSON dict is parsed
- **THEN** it is returned directly as `extracted_requirements` bypassing normalisation and filtering (passthrough path)

#### Scenario: Non-compliant JSON uploaded
- **WHEN** the JSON has a list root, nested dicts, or non-string values
- **THEN** a `NonStandardJSONError` is raised detailing the structural violation and offending keys
