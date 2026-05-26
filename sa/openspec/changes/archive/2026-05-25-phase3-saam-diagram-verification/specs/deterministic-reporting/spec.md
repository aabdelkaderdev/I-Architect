## MODIFIED Requirements

### Requirement: JSON Report Output
The system SHALL export the structured `ScoringReport` as a JSON file to the provided output path, including all gap analysis data.

#### Scenario: JSON Export
- **WHEN** Node 5 completes execution
- **THEN** it writes `scoring_report.json` to the target directory containing the full schema, including `diagram_issues` populated from Node 4
