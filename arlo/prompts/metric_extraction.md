{{! Metric Extraction Prompt — Prompt #2 (DISABLED) }}
{{! C# Source: RequirementParser.cs L156 }}
{{! Status: Currently disabled in C# source (line L125). }}
{{! Preserved for future activation. }}

For each condition in the provided list, extract all metrics (e.g., `"user numbers"`, `"bandwidth"`) and the value or quality specified for them (e.g., `"increases significantly"`, `"below 50MB/s"`).

> Output structure is enforced externally. Populate each field accurately:
> `id`, `triggers` — where each trigger contains: `metric`, `trigger`
