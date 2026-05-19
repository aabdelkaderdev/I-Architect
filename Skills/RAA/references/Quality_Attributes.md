# Quality Attributes — Adapted for RAA

## Purpose

Defines the ISO/IEC 25010 quality attributes used by the I-Architect pipeline. These attributes inform ARLO quality weight assignment, SAAM scenario derivation, and architectural pattern selection.

> **Source:** ISO/IEC 25010:2011 — Systems and software Quality Requirements and Evaluation (SQuaRE)
>
> **Adaptation notice:** The 8 attributes below are the pipeline's working taxonomy. Each attribute is defined with representative ASR condition examples and scenario-evaluation prompts for SAAM scoring.

## Quality Attributes

### Performance Efficiency
Achieving high performance under economic resource utilization.

**ASR condition examples:** "when the system is under peak load," "during concurrent user spikes," "with large datasets."

**SAAM scenario prompt:** Define a scenario describing the system under a measurable performance constraint (e.g., "process 10,000 requests per second"). Evaluate whether each architectural structure can meet this constraint.

### Compatibility
Interoperability and co-existence with other systems.

**ASR condition examples:** "when integrating with the legacy ERP," "across heterogeneous platforms," "during API version transitions."

**SAAM scenario prompt:** Define a scenario requiring data exchange or co-existence with an external system. Evaluate whether each structure supports the required protocols and data formats.

### Usability
A user-friendly application with straightforward and elegant UX and UI.

**ASR condition examples:** "for non-technical users," "in mobile contexts," "when onboarding new users."

**SAAM scenario prompt:** Define a scenario describing a user interaction flow (e.g., "a first-time user completes checkout"). Evaluate whether each structure supports the required user-facing capabilities.

### Reliability
Stability under different conditions.

**ASR condition examples:** "when network connectivity is intermittent," "during hardware failures," "under prolonged operation."

**SAAM scenario prompt:** Define a failure scenario (e.g., "database becomes unreachable for 30 seconds"). Evaluate whether each structure continues to meet its functional obligations.

### Security
Protecting data, preventing breaches.

**ASR condition examples:** "when handling PII," "for financial transactions," "when accessed from untrusted networks."

**SAAM scenario prompt:** Define a threat scenario (e.g., "an attacker attempts SQL injection through the login form"). Evaluate whether each structure provides appropriate controls.

### Maintainability
Easy to modify and improve.

**ASR condition examples:** "when adding new payment providers," "for configuration changes without redeployment," "with frequent requirement changes."

**SAAM scenario prompt:** Define a modification scenario (e.g., "replace the payment processor integration"). Evaluate how many structures must change to accommodate it.

### Portability
Adaptable to different environments.

**ASR condition examples:** "across cloud providers," "when migrating from on-premise to cloud," "for containerized deployment."

**SAAM scenario prompt:** Define a deployment scenario on a different target platform. Evaluate whether each structure is environment-agnostic.

### Cost Efficiency
Keep the overall cost (including development, operations, and maintenance) as low as possible.

**ASR condition examples:** "when minimizing cloud infrastructure costs," "for a lean team," "during early-stage startup scaling."

**SAAM scenario prompt:** Define a resource-constrained scenario (e.g., "the budget allows for two server instances"). Evaluate whether each structure minimizes unnecessary resource consumption.
