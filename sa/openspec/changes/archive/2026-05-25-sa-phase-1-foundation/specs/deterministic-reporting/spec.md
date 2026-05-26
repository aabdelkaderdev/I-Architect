## ADDED Requirements

### Requirement: Report Grade Calculation
The system SHALL sum the three axis scores and assign a letter grade (A: 90+, B: 80+, C: 70+, D: 60+, F: <60).

#### Scenario: Grade Assignment
- **WHEN** the total score is computed from the state axes
- **THEN** the correct letter grade is assigned based on the thresholds

### Requirement: JSON Report Output
The system SHALL export the structured `ScoringReport` as a JSON file to the provided output path.

#### Scenario: JSON Export
- **WHEN** Node 5 completes execution
- **THEN** it writes `scoring_report.json` to the target directory containing the full schema
