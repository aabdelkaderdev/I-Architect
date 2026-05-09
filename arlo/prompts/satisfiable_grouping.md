{{! Satisfiable Grouping Prompt — Prompt #4 }}
{{! C# Source: Architect.cs L366–369 }}
{{! Strategy: Symbolic ID grounding — LLM reasons on numeric IDs }}
{{! Output enforced by SatGroup Pydantic model → [[1,2],[3,4]] }}

Organize the provided set of conditions into groups where all conditions within the same group can be true at the same time. Return only the IDs of the conditions in each group.

Rules:
1. A condition may appear in more than one group.
2. If a condition is `"under any circumstances"`, include it in every group.
3. Return IDs only — no condition text, no explanation, nothing before or after.

Conditions:
{{conditions}}

> Output structure is enforced externally. Example: `((1,2),(3,4))`
