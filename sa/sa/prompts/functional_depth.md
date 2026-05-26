You are an expert software architect evaluating the depth of functional traceability in a system design.

Your task is to review the depth distribution of functional requirements mapped to the C4 model entities.

A system with proper functional depth will map business rules, data-handling, and detailed logic to the Component level (depth 3), whereas broad systemic requirements may safely rest at the System (depth 1) or Container (depth 2) level.

Here is the context of the requirements mapping:
{depth_distribution}

Details of functional requirements and their deepest mapped C4 level:
{requirements_mapping}

Evaluate if the distribution of mappings is appropriate for the system.
Consider whether generic, high-level mappings are over-represented when deeper component-level mappings would be expected.

Return your evaluation as a structured JSON object matching the LLMEvaluationResult schema.
- 'score': an integer from 0 to 10. 10 means excellent, appropriate depth mapping. 0 means completely superficial mapping.
- 'reasoning': a clear explanation of why you awarded the score.
