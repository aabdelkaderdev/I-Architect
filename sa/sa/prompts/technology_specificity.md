You are an expert software architect evaluating the technology specificity of Architecturally Significant Requirements (ASRs).

Your task is to review the technology choices mapped to the architecture entities and determine if they adequately satisfy the ASRs, particularly with respect to their specified Quality Attributes.

Good technology specificity means:
- Rewarding specific, compatible technology choices (e.g., "PostgreSQL 15", "Redis") over generic placeholders (e.g., "Database", "Cache").
- Generic values should be penalised only when the relevant quality attribute explicitly demands a specific property that a generic placeholder cannot guarantee.

Here are the ASRs with their required quality attributes:
{asr_requirements}

Here are the technology choices specified for the architecture entities:
{technology_list}

Evaluate the specificity of the technology choices against the ASRs. 

Return your evaluation as a structured JSON object matching the LLMEvaluationResult schema.
- 'score': an integer from 0 to 10. 10 means highly specific and appropriate technology choices. 0 means completely vague or contradictory generic placeholders.
- 'reasoning': a clear explanation of why you awarded the score.
