{{! ASR Classification Prompt — Prompt #1 }}
{{! Modes: stringent (both conditions) or lax (quality attributes only) }}
{{! C# Source: RequirementParser.cs L67–91 }}
I have provided a set of software requirements. Extract the following information and return a JSON array of requirement objects.

{{#stringent}}
**1. Whether it is architecturally-significant.** A requirement is architecturally-significant only if it satisfies **both** conditions:
1. It explicitly states a key decision regarding high-level software architecture.
2. It specifies one or more of the following quality attributes:
{{/stringent}}
{{^stringent}}
**1. Whether it is architecturally-significant.** A requirement is architecturally-significant if it specifies one or more of the following quality attributes regarding overall software architecture *(not considered architecturally-significant if it concerns an aspect of the software that does not impact its architecture)*:
{{/stringent}}

{{#quality_attributes}}
- **{{name}}**: {{description}}
{{/quality_attributes}}

**2.** Identify any quality attributes from the list above only. *(Do not include anything outside of the above list.)*

**3.** The `condition_text` is a conditional statement in the requirement describing when the quality attributes apply (e.g. `"if bandwidth is low"`, `"when traffic is high"`, `"all the time"`). Return `"N/A"` if none is present.

> Output structure is enforced externally. Populate each field accurately:
> `id`, `is_architecturally_significant`, `quality_attributes`, `condition_text`
