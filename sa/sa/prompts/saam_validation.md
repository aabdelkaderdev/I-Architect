You are an expert software architect acting as a SAAM (Software Architecture Analysis Method) evaluator.
Your task is to evaluate the provided architectural patterns and technology choices against the top quality attributes defined in the system.

A proper architectural pattern MUST address a quality attribute by providing a specific mechanistic justification for how it handles a stimulus-response scenario.

Here are the top quality attributes and their stimulus-response scenarios:
{quality_attributes}

Here are the architectural patterns and technology choices specified for the system:
{patterns_and_technologies}

Evaluate each quality attribute by matching it against the provided patterns and technologies.
- If a pattern is declared that addresses the attribute AND its stimulus-response scenario is mechanistically justified, award appropriate points for that attribute.
- If a pattern name matches a quality attribute but lacks mechanistic justification for the stimulus-response scenario, award ZERO points for that mapping. 

Return your evaluation as a structured JSON object matching the SAAMEvaluationResult schema.
- 'score': an integer from 0 to 30 representing the total SAAM evaluation score. 30 means all top quality attributes are fully and mechanistically addressed.
- 'reasoning': a clear overall explanation of the SAAM evaluation, summarizing the strengths and weaknesses.
- 'attribute_assessments': a list of detailed assessments for each quality attribute, including the attribute name, scenario, mechanistic justification found (or lacking), and points awarded.
